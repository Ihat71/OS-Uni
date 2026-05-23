"""
routers/submissions.py
Endpoints for managing student file submissions.

Workflow:
  1. Student (or manager on their behalf) POST /api/submissions/
     → registers the submission, sets status = "received"
  2. Manager reviews the file, then PATCH /api/submissions/{task_id}
     → updates status to "approved" or "broken"
  3. GET /api/submissions/dashboard
     → manager sees overall progress at a glance
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone

from models.schemas import (
    SubmissionCreate,
    SubmissionUpdate,
    SubmissionResponse,
    DashboardSummary,
    TOPICS,
)
from routers.pages import update_page_record, _page_store   # share the same store

router = APIRouter()

# Separate notes store (keeps page records clean)
_notes: dict[int, str | None] = {}


@router.post(
    "/",
    response_model=SubmissionResponse,
    status_code=201,
    summary="Register a student submission",
)
async def create_submission(body: SubmissionCreate):
    """
    Call this when a student sends their HTML file.
    Sets the page status to 'received' and records who submitted it.
    Returns 409 if that task was already submitted.
    """
    page = _page_store.get(body.task_id)
    if page is None:
        raise HTTPException(status_code=404, detail=f"Task {body.task_id} not found")

    if page["status"] != "pending":
        raise HTTPException(
            status_code=409,
            detail=f"Task {body.task_id} already has a submission "
                   f"(status: {page['status']}). Use PATCH to update it.",
        )

    now = datetime.now(timezone.utc)
    updated = update_page_record(body.task_id, {
        "student_name": body.student_name,
        "filename": body.filename,
        "status": "received",
        "submitted_at": now,
    })
    _notes[body.task_id] = None

    return SubmissionResponse(
        task_id=updated["task_id"],
        topic_name=updated["topic_name"],
        student_name=updated["student_name"],
        filename=updated["filename"],
        status=updated["status"],
        submitted_at=updated["submitted_at"],
        notes=_notes.get(body.task_id),
    )


@router.patch(
    "/{task_id}",
    response_model=SubmissionResponse,
    summary="Update submission status (manager only)",
)
async def update_submission(task_id: int, body: SubmissionUpdate):
    """
    Manager sets status to 'approved' (page works correctly)
    or 'broken' (student needs to fix and resubmit).
    Optional notes field for feedback.
    """
    page = _page_store.get(task_id)
    if page is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    if page["status"] == "pending":
        raise HTTPException(
            status_code=400,
            detail="Cannot update a task that has no submission yet.",
        )

    updated = update_page_record(task_id, {"status": body.status})
    _notes[task_id] = body.notes

    return SubmissionResponse(
        task_id=updated["task_id"],
        topic_name=updated["topic_name"],
        student_name=updated["student_name"],
        filename=updated["filename"],
        status=updated["status"],
        submitted_at=updated["submitted_at"],
        notes=_notes.get(task_id),
    )


@router.get(
    "/dashboard",
    response_model=DashboardSummary,
    summary="Manager dashboard — submission progress",
)
async def get_dashboard():
    """
    Returns a quick count of how many pages are in each status.
    Use this to check how close the class is to the May 22 deadline.
    """
    statuses = [p["status"] for p in _page_store.values()]
    approved  = statuses.count("approved")
    received  = statuses.count("received")
    broken    = statuses.count("broken")
    pending   = statuses.count("pending")
    done      = approved + received          # pages the manager actually has

    return DashboardSummary(
        approved=approved,
        received=received,
        broken=broken,
        pending=pending,
        completion_percentage=round(done / 30 * 100, 1),
    )


@router.get(
    "/",
    response_model=list[SubmissionResponse],
    summary="List all received submissions",
)
async def list_submissions():
    """Returns every task that has been submitted (status != pending)."""
    result = []
    for page in _page_store.values():
        if page["status"] != "pending":
            result.append(SubmissionResponse(
                task_id=page["task_id"],
                topic_name=page["topic_name"],
                student_name=page["student_name"],
                filename=page["filename"],
                status=page["status"],
                submitted_at=page["submitted_at"],
                notes=_notes.get(page["task_id"]),
            ))
    return result

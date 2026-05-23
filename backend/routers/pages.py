"""
routers/pages.py
Endpoints for browsing the topic catalogue and individual pages.
"""

from fastapi import APIRouter, HTTPException
from models.schemas import PageInfo, TOPICS
router = APIRouter()

# In a real deployment swap this in-memory store for a SQLite/Postgres table.
# Key: task_id  Value: PageInfo dict
_page_store: dict[int, dict] = {
    task_id: {
        "task_id": task_id,
        "topic_name": name,
        "filename": f"task{task_id:02d}_{name.lower().replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_')[:30]}.html",
        "student_name": None,
        "status": "pending",
        "submitted_at": None,
    }
    for task_id, name in TOPICS.items()
}


@router.get("/", response_model=list[PageInfo], summary="List all topic pages")
async def list_pages(status: str | None = None):
    """
    Return all 30 topic pages.
    Optionally filter by status: pending | received | broken | approved
    """
    pages = list(_page_store.values())
    if status:
        pages = [p for p in pages if p["status"] == status]
    return pages



@router.get("/{task_id}", response_model=PageInfo, summary="Get one topic page")
async def get_page(task_id: int):
    if task_id not in _page_store:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return _page_store[task_id]


# ── Internal helper used by the submissions router ────────────────────────────

def update_page_record(task_id: int, updates: dict) -> dict:
    if task_id not in _page_store:
        raise KeyError(f"Task {task_id} does not exist")
    _page_store[task_id].update(updates)
    return _page_store[task_id]

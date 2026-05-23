"""
models/schemas.py
Pydantic models shared across routers.
"""

from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


# ── Topic catalogue (all 30 assignments) ──────────────────────────────────────

TOPICS: dict[int, str] = {
    1:  "FCFS CPU Scheduler",
    2:  "SJF CPU Scheduler",
    3:  "Priority Scheduling (Preemptive)",
    4:  "Priority Scheduling (Non-Preemptive)",
    5:  "Preemptive vs. Non-Preemptive Scheduling",
    6:  "Process States",
    7:  "Process Control Block (PCB)",
    8:  "Context Switching",
    9:  "IPC: Shared Memory Model",
    10: "IPC: Message Passing Model",
    11: "Direct Memory Access (DMA)",
    12: "Linker and Loader",
    13: "Deadlocks",
    14: "Virtual Memory and Paging",
    15: "Threading",
    16: "Parallelism",
    17: "Concurrency",
    18: "Multithreading Models",
    19: "When is Multithreading Beneficial?",
    20: "OS as a Bridge: Hardware and Software",
    21: "User Mode vs. Kernel Mode",
    22: "Interrupts",
    23: "lseek()",
    24: "fork()",
    25: "wait()",
    26: "exit()",
    27: "sleep()",
    28: "dup() and dup2()",
    29: "read()",
    30: "write()",
}

SubmissionStatus = Literal["pending", "received", "broken", "approved"]


# ── Request / Response schemas ─────────────────────────────────────────────────

class PageInfo(BaseModel):
    """Metadata about one topic page."""
    task_id: int = Field(..., ge=1, le=30, description="Topic number (1-30)")
    topic_name: str
    filename: str                   # e.g. "task14_paging.html"
    student_name: str | None = None
    status: SubmissionStatus = "pending"
    submitted_at: datetime | None = None

    model_config = {"from_attributes": True}


class SubmissionCreate(BaseModel):
    """Body sent when a student registers their submission."""
    task_id: int = Field(..., ge=1, le=30)
    student_name: str = Field(..., min_length=2, max_length=120)
    filename: str = Field(
        ...,
        pattern=r"^[\w\-]+\.html$",
        description="HTML filename, e.g. task14_paging.html",
    )


class SubmissionUpdate(BaseModel):
    """Body for the manager to update a submission's status."""
    status: SubmissionStatus
    notes: str | None = None


class SubmissionResponse(BaseModel):
    """What the API returns after a submission action."""
    task_id: int
    topic_name: str
    student_name: str
    filename: str
    status: SubmissionStatus
    submitted_at: datetime
    notes: str | None = None


class DashboardSummary(BaseModel):
    """High-level stats for the manager's dashboard."""
    total_tasks: int = 30
    approved: int
    received: int
    broken: int
    pending: int
    completion_percentage: float

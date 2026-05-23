import { notes, pageStore, updatePageRecord } from "./store.js";
import { STATUSES } from "./topics.js";
import {
  parseTaskId,
  validateSubmissionCreate,
  validateSubmissionUpdate,
} from "./validation.js";

function submissionResponse(page, taskId) {
  return {
    task_id: page.task_id,
    topic_name: page.topic_name,
    student_name: page.student_name,
    filename: page.filename,
    status: page.status,
    submitted_at: page.submitted_at,
    notes: notes[taskId] ?? null,
  };
}

export function registerRoutes(app) {
  app.get("/health", (c) =>
    c.json({
      status: "ok",
      server_time_utc: new Date().toISOString(),
      project: "OS Interactive Web Portfolio",
    }),
  );

  app.get("/pages", (c) => {
    const status = c.req.query("status");
    let pages = Object.values(pageStore);
    if (status) {
      if (!STATUSES.includes(status)) {
        return c.json(
          { detail: `status must be one of: ${STATUSES.join(", ")}` },
          400,
        );
      }
      pages = pages.filter((p) => p.status === status);
    }
    return c.json(pages);
  });

  app.get("/pages/:taskId", (c) => {
    const taskId = parseTaskId(c.req.param("taskId"));
    if (taskId === null) {
      return c.json({ detail: "Invalid task_id" }, 400);
    }
    const page = pageStore[taskId];
    if (!page) {
      return c.json({ detail: `Task ${taskId} not found` }, 404);
    }
    return c.json(page);
  });

  app.get("/submissions/dashboard", (c) => {
    const statuses = Object.values(pageStore).map((p) => p.status);
    const approved = statuses.filter((s) => s === "approved").length;
    const received = statuses.filter((s) => s === "received").length;
    const broken = statuses.filter((s) => s === "broken").length;
    const pending = statuses.filter((s) => s === "pending").length;
    const done = approved + received;

    return c.json({
      total_tasks: 30,
      approved,
      received,
      broken,
      pending,
      completion_percentage: Math.round((done / 30) * 1000) / 10,
    });
  });

  app.get("/submissions", (c) => {
    const result = Object.values(pageStore)
      .filter((p) => p.status !== "pending")
      .map((p) => submissionResponse(p, p.task_id));
    return c.json(result);
  });

  app.post("/submissions", async (c) => {
    let body;
    try {
      body = await c.req.json();
    } catch {
      return c.json({ detail: "Invalid JSON body" }, 400);
    }

    const errors = validateSubmissionCreate(body);
    if (errors.length) {
      return c.json({ detail: errors.join("; ") }, 422);
    }

    const taskId = Number(body.task_id);
    const page = pageStore[taskId];
    if (!page) {
      return c.json({ detail: `Task ${taskId} not found` }, 404);
    }

    if (page.status !== "pending") {
      return c.json(
        {
          detail: `Task ${taskId} already has a submission (status: ${page.status}). Use PATCH to update it.`,
        },
        409,
      );
    }

    const now = new Date().toISOString();
    const updated = updatePageRecord(taskId, {
      student_name: body.student_name,
      filename: body.filename,
      status: "received",
      submitted_at: now,
    });
    notes[taskId] = null;

    return c.json(submissionResponse(updated, taskId), 201);
  });

  app.patch("/submissions/:taskId", async (c) => {
    const taskId = parseTaskId(c.req.param("taskId"));
    if (taskId === null) {
      return c.json({ detail: "Invalid task_id" }, 400);
    }

    let body;
    try {
      body = await c.req.json();
    } catch {
      return c.json({ detail: "Invalid JSON body" }, 400);
    }

    const errors = validateSubmissionUpdate(body);
    if (errors.length) {
      return c.json({ detail: errors.join("; ") }, 422);
    }

    const page = pageStore[taskId];
    if (!page) {
      return c.json({ detail: `Task ${taskId} not found` }, 404);
    }

    if (page.status === "pending") {
      return c.json(
        { detail: "Cannot update a task that has no submission yet." },
        400,
      );
    }

    const updated = updatePageRecord(taskId, { status: body.status });
    notes[taskId] = body.notes ?? null;

    return c.json(submissionResponse(updated, taskId));
  });
}

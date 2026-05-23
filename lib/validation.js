import { STATUSES, TOPICS } from "./topics.js";

const HTML_FILENAME = /^[\w\-]+\.html$/;

export function parseTaskId(value) {
  const taskId = Number(value);
  if (!Number.isInteger(taskId) || taskId < 1 || taskId > 30) {
    return null;
  }
  return taskId;
}

export function validateSubmissionCreate(body) {
  const errors = [];
  if (!body || typeof body !== "object") {
    return ["Request body must be a JSON object"];
  }

  const taskId = parseTaskId(body.task_id);
  if (taskId === null) {
    errors.push("task_id must be an integer between 1 and 30");
  } else if (!(taskId in TOPICS)) {
    errors.push(`Task ${taskId} not found`);
  }

  const name = body.student_name;
  if (typeof name !== "string" || name.length < 2 || name.length > 120) {
    errors.push("student_name must be a string between 2 and 120 characters");
  }

  const filename = body.filename;
  if (typeof filename !== "string" || !HTML_FILENAME.test(filename)) {
    errors.push("filename must match pattern: word chars, hyphens, ending in .html");
  }

  return errors;
}

export function validateSubmissionUpdate(body) {
  const errors = [];
  if (!body || typeof body !== "object") {
    return ["Request body must be a JSON object"];
  }

  if (!STATUSES.includes(body.status)) {
    errors.push(`status must be one of: ${STATUSES.join(", ")}`);
  }

  if (body.notes !== undefined && body.notes !== null && typeof body.notes !== "string") {
    errors.push("notes must be a string or null");
  }

  return errors;
}

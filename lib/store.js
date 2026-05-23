import { TOPICS } from "./topics.js";

function defaultFilename(taskId, name) {
  const slug = name
    .toLowerCase()
    .replace(/ /g, "_")
    .replace(/[()]/g, "")
    .replace(/\//g, "_")
    .slice(0, 30);
  return `task${String(taskId).padStart(2, "0")}_${slug}.html`;
}

function buildPageStore() {
  const store = {};
  for (const [id, name] of Object.entries(TOPICS)) {
    const taskId = Number(id);
    store[taskId] = {
      task_id: taskId,
      topic_name: name,
      filename: defaultFilename(taskId, name),
      student_name: null,
      status: "pending",
      submitted_at: null,
    };
  }
  return store;
}

/** @type {Record<number, object>} */
export const pageStore = buildPageStore();

/** @type {Record<number, string | null>} */
export const notes = {};

export function updatePageRecord(taskId, updates) {
  if (!(taskId in pageStore)) {
    throw new Error(`Task ${taskId} does not exist`);
  }
  Object.assign(pageStore[taskId], updates);
  return pageStore[taskId];
}

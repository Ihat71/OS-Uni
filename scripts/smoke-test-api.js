import { Hono } from "hono";
import { registerRoutes } from "../lib/routes.js";

const app = new Hono().basePath("/api");
registerRoutes(app);

async function check(path, init) {
  const res = await app.request(path, init);
  const body = await res.json();
  console.log(res.status, path, JSON.stringify(body).slice(0, 120));
  return res.status;
}

const health = await check("/api/health");
const pages = await check("/api/pages");
const dash = await check("/api/submissions/dashboard");

if (health !== 200 || pages !== 200 || dash !== 200) {
  process.exit(1);
}

console.log("API smoke test passed");

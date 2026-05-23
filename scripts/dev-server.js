/**
 * Local dev server — mirrors Vercel (static public/ + /api routes).
 * No Vercel account required. Use: npm start
 */

import { serve } from "@hono/node-server";
import { serveStatic } from "@hono/node-server/serve-static";
import { Hono } from "hono";
import { cors } from "hono/cors";
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { registerRoutes } from "../lib/routes.js";

const __dirname = dirname(fileURLToPath(import.meta.url));
const projectRoot = join(__dirname, "..");
const publicDir = join(projectRoot, "public");
const port = Number(process.env.PORT) || 3000;

if (!existsSync(publicDir)) {
  console.error("public/ not found. Run: npm run build");
  process.exit(1);
}

const app = new Hono();

app.use(
  "*",
  cors({
    origin: "*",
    allowMethods: ["GET", "POST", "PATCH", "OPTIONS"],
    allowHeaders: ["*"],
  }),
);

const api = new Hono().basePath("/api");
registerRoutes(api);
app.route("/", api);

app.get("/", serveStatic({ path: "./public/index.html" }));
app.use("/pages/*", serveStatic({ root: "./public/" }));
app.use("/*", serveStatic({ root: "./public/" }));

console.log(`OS Portfolio dev server → http://localhost:${port}`);
console.log(`  Site:  http://localhost:${port}/`);
console.log(`  API:   http://localhost:${port}/api/health`);

serve({ fetch: app.fetch, port });

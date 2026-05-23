import { Hono } from "hono";
import { cors } from "hono/cors";
import { handle } from "hono/vercel";
import { registerRoutes } from "../lib/routes.js";

const app = new Hono().basePath("/api");

app.use(
  "*",
  cors({
    origin: "*",
    allowMethods: ["GET", "POST", "PATCH", "OPTIONS"],
    allowHeaders: ["*"],
  }),
);

registerRoutes(app);

export default handle(app);

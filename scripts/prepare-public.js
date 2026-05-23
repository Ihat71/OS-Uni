/** Copy frontend assets into public/ for Vercel static hosting. */

import { cpSync, existsSync, mkdirSync, rmSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const projectRoot = join(__dirname, "..");
const frontendDir = join(projectRoot, "frontend");
const publicDir = join(projectRoot, "public");

if (!existsSync(frontendDir)) {
  console.warn(`Warning: ${frontendDir} not found, skipping static copy.`);
  process.exit(0);
}

if (existsSync(publicDir)) {
  rmSync(publicDir, { recursive: true, force: true });
}

mkdirSync(publicDir, { recursive: true });

cpSync(join(frontendDir, "index.html"), join(publicDir, "index.html"));

const pagesSrc = join(frontendDir, "pages");
if (existsSync(pagesSrc)) {
  cpSync(pagesSrc, join(publicDir, "pages"), { recursive: true });
}

console.log(`Prepared Vercel static assets in ${publicDir}`);

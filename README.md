# Operating Systems Final Class Project

## Overview

The Operating Systems final class project is meant to act as a study guide of sorts for the newer generations after us and we, the future CE and CS class of 2027, are more than happy to leave our mark on this course. It's like a passing of the torch from the better students to the worse ones. To our juniors: since we already completed this course WE are all better than you (at least for now), don't forget that.

## Tech Stack

1. **Node.js + [Hono](https://hono.dev)** — API routes (`/api/*`) deployed as a Vercel serverless function
2. **HTML/CSS/JS** — static portfolio pages in `frontend/`

## Project layout

```
os-uni-project/
  frontend/          # Source static site (edit here)
  public/            # Built copy for Vercel (generated, gitignored)
  api/index.js       # Vercel serverless entry — all API routes
  lib/               # Topics catalogue, in-memory store, route handlers
  scripts/           # Build helpers
  vercel.json        # Vercel project config
```

## API (same as before)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/pages` | List all 30 topic pages (`?status=` optional) |
| GET | `/api/pages/:taskId` | One page metadata |
| POST | `/api/submissions` | Register a student submission |
| PATCH | `/api/submissions/:taskId` | Manager updates status |
| GET | `/api/submissions/dashboard` | Progress summary |
| GET | `/api/submissions` | All non-pending submissions |

Submission data is kept **in memory** inside the serverless function. It resets when the function cold-starts. For production persistence, add Vercel KV, Postgres, or similar.

## Local development (test before deploy)

**Recommended — no Vercel login:**

```bash
cd os-uni-project
npm install
npm run build    # copies frontend/ → public/
npm start        # http://localhost:3000
```

Check in the browser:

- Home: `http://localhost:3000/`
- A task page: `http://localhost:3000/pages/task1_fcfs.html`
- API health: `http://localhost:3000/api/health`
- All pages: `http://localhost:3000/api/pages`

**Optional — full Vercel emulator** (requires `npx vercel login` once):

```bash
npm run build
npm run dev
```

Static-only preview (no API):

```bash
npm run build
npx serve public
```

## Deploy on Vercel

1. Push this repo to GitHub.
2. Import the project in [Vercel](https://vercel.com) — root directory: `os-uni-project` (or repo root if this is the only project).
3. Vercel detects `vercel.json`: build runs `npm run build`, static files go to `public/`, API lives under `/api`.

No Python runtime required.

## Features

The website includes all the material and concepts studied in the OS course in UKH.

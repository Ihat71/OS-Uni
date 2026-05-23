from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from paths import FRONTEND_INDEX, FRONTEND_PAGES, IS_VERCEL
from routers import pages, submissions, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    print("✅ OS Portfolio server starting up...")
    yield
    print("🛑 OS Portfolio server shutting down...")


app = FastAPI(
    title="OS Interactive Web Portfolio",
    description="Backend for the Operating Systems class capstone website. "
                "Manages student page submissions and serves the unified site.",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(health.router,       prefix="/api",       tags=["Health"])
app.include_router(pages.router,        prefix="/api/pages", tags=["Pages"])
app.include_router(submissions.router,  prefix="/api/submissions", tags=["Submissions"])

# ── Static files (local dev only) ─────────────────────────────────────────────
# On Vercel, static assets are copied to public/ during build and served by the CDN.
if not IS_VERCEL:
    if FRONTEND_PAGES.is_dir():
        app.mount(
            "/pages",
            StaticFiles(directory=str(FRONTEND_PAGES)),
            name="pages",
        )

    @app.get("/", include_in_schema=False)
    async def serve_index():
        if FRONTEND_INDEX.is_file():
            return FileResponse(str(FRONTEND_INDEX))
        raise HTTPException(status_code=404, detail="index.html not found")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

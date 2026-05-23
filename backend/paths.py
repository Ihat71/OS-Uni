"""Shared path helpers for local dev and Vercel deployment."""

from pathlib import Path
import os

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
FRONTEND_PAGES = FRONTEND_DIR / "pages"
FRONTEND_INDEX = FRONTEND_DIR / "index.html"
PUBLIC_DIR = BACKEND_DIR / "public"
PUBLIC_PAGES = PUBLIC_DIR / "pages"

IS_VERCEL = os.getenv("VERCEL") == "1"

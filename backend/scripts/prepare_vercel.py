"""Copy frontend assets into public/ for Vercel CDN serving."""

import shutil
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
PUBLIC_DIR = BACKEND_DIR / "public"


def main() -> None:
    if not FRONTEND_DIR.is_dir():
        print(f"Warning: {FRONTEND_DIR} not found, skipping static copy.")
        return

    if PUBLIC_DIR.exists():
        shutil.rmtree(PUBLIC_DIR)

    PUBLIC_DIR.mkdir(parents=True)

    index = FRONTEND_DIR / "index.html"
    if index.is_file():
        shutil.copy2(index, PUBLIC_DIR / "index.html")

    pages_src = FRONTEND_DIR / "pages"
    if pages_src.is_dir():
        shutil.copytree(pages_src, PUBLIC_DIR / "pages")

    print(f"Prepared Vercel static assets in {PUBLIC_DIR}")


if __name__ == "__main__":
    main()

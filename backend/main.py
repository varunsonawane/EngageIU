import os
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import engine, SessionLocal, init_db
from models import EndpointPerformance


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB + seed on startup
    init_db()
    db = SessionLocal()
    try:
        from seed import seed_data
        seed_data(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="EngageIU API",
    version="1.0.0",
    description=(
        "QR/code-based campus event attendance leaderboard system for Indiana University. "
        "Students earn points by entering check-in codes at IU events."
    ),
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Performance tracking middleware ─────────────────────────────────────────
@app.middleware("http")
async def track_performance(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000

    # Skip recording performance entries for the /performance endpoint itself
    # and static file requests to avoid noise
    path = request.url.path
    skip_prefixes = ("/static", "/favicon", "/openapi", "/docs", "/redoc")
    if not any(path.startswith(p) for p in skip_prefixes):
        db: Session = SessionLocal()
        try:
            perf = EndpointPerformance(
                endpoint=path,
                method=request.method,
                response_time_ms=round(elapsed_ms, 3),
                called_at=datetime.now(timezone.utc).replace(tzinfo=None),
            )
            db.add(perf)
            db.commit()
        except Exception:
            db.rollback()
        finally:
            db.close()

    return response


# ── Routers ──────────────────────────────────────────────────────────────────
from routers import auth, leaderboard, events  # noqa: E402

app.include_router(auth.router, tags=["auth"])
app.include_router(leaderboard.router, tags=["leaderboard"])
app.include_router(events.router, tags=["events"])

# ── Static frontend files ─────────────────────────────────────────────────
# FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_index():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

    @app.get("/events-page", include_in_schema=False)
    async def serve_events():
        return FileResponse(os.path.join(FRONTEND_DIR, "events.html"))

    @app.get("/admin", include_in_schema=False)
    async def serve_admin():
        return FileResponse(os.path.join(FRONTEND_DIR, "admin.html"))
if os.path.isdir(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_index():
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

    @app.get("/events-page", include_in_schema=False)
    async def serve_events():
        return FileResponse(os.path.join(FRONTEND_DIR, "events.html"))

    @app.get("/admin", include_in_schema=False)
    async def serve_admin():
        return FileResponse(os.path.join(FRONTEND_DIR, "admin.html"))

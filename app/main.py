"""FastAPI alkalmazás; kizárólag 127.0.0.1:8765-ön figyel (L7, NFR-02)."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import health, jobs, lexicon, outputs, projects, reader, voices
from app.state import AppState, setup_logging

HOST = "127.0.0.1"
PORT = 8765

log = logging.getLogger(__name__)


def create_app(state: AppState | None = None, start_queue: bool = True) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        st = app.state.app
        if start_queue:
            st.start()
        yield
        if start_queue:
            st.stop()

    app = FastAPI(title="Zengő", version="1.0.0", lifespan=lifespan)
    app.state.app = state or AppState()
    for r in (health.router, projects.router, jobs.router, voices.router, lexicon.router, outputs.router,
              reader.router):
        app.include_router(r)
    try:
        from app.web.routes import mount_web

        mount_web(app)
    except ImportError:
        pass
    return app


def run() -> None:
    import argparse

    import uvicorn

    parser = argparse.ArgumentParser(prog="felolvaso")
    parser.add_argument("--port", type=int, default=PORT, help="port (alapértelmezés: 8765)")
    args = parser.parse_args()
    state = AppState()
    setup_logging(state.config)
    state.init_qa()
    log.info("Zengő indul: http://%s:%d", HOST, args.port)
    uvicorn.run(create_app(state), host=HOST, port=args.port, log_level="info")


if __name__ == "__main__":
    run()

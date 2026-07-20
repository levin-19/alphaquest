"""
app.py — Main FastAPI application factory for AlphaQuest API.

Responsibilities:
  - Initialize FastAPI with metadata.
  - Register CORS middleware.
  - Register security headers middleware.
  - Register startup / shutdown lifecycle hooks.
  - Register all API routes.
  - Install global exception handlers.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes import router
from config import settings
from core.logger import get_logger
from core.model_loader import model_manager
from core.security import SecurityHeadersMiddleware

logger = get_logger("App")


# ---------------------------------------------------------------------------
# Lifespan (startup + shutdown)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage startup and shutdown events.
    Models are loaded once here and reused for the lifetime of the process.
    """
    logger.info("Server Started")
    model_manager.load_all()   # Loads models + labels into memory (once)
    yield
    logger.info("Server shutting down. Resources released.")


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    description=(
        "Production-ready AI backend for the AlphaQuest children's education app. "
        "Exposes endpoints for alphabet image recognition and speech recognition "
        "powered by TensorFlow models."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Security headers on every response
app.add_middleware(SecurityHeadersMiddleware)

# CORS — allow all origins so the Flutter app can connect from any device
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all route handlers
app.include_router(router)


# ---------------------------------------------------------------------------
# Global exception handlers
# ---------------------------------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all handler that prevents raw stack traces from reaching the client.
    Internal errors are logged server-side and returned as clean JSON.
    """
    logger.error(f"Unhandled exception on {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "An internal server error occurred."},
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc) -> JSONResponse:
    """Return a clean JSON 404 instead of the default HTML page."""
    return JSONResponse(
        status_code=404,
        content={"error": f"Endpoint '{request.url.path}' not found."},
    )

"""
startup.py — Standalone entry point for running AlphaQuest API locally or on Render.
Render uses the command in render.yaml instead, but this file allows `python startup.py`.
"""
import os

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=False,       # Never use reload=True in production
        log_level="info",
    )

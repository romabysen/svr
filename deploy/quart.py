import os

bind = f"0.0.0.0:{os.getenv("PORT", "8000")}"
workers = os.getenv("HYPERCORN_WORKERS", "1")

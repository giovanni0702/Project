"""Run locally: PARKING_CITY=<city> python -m backend. Access log is off (C7: no IP in logs)."""
import uvicorn

from .app import create_app

if __name__ == "__main__":
    uvicorn.run(create_app(), host="127.0.0.1", port=8000, access_log=False, log_level="warning")

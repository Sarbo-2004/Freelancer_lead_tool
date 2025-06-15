import asyncio
import sys

# ✅ Fix for Playwright async on Windows
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI
from dotenv import load_dotenv
from routers import leads, leads_route

load_dotenv()

app = FastAPI(title="Freelancer Lead Finder & Auditor")

# Register your routers
app.include_router(leads.router, prefix="/api")
app.include_router(leads_route.router, prefix="/api")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to freelancer lead tool backend"}

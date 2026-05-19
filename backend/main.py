from fastapi import FastAPI
from database import init_db
from routers.files import router as files_router
from routers.stages import router as stages_router

app = FastAPI(title="SDD Platform")


@app.on_event("startup")
async def startup():
    await init_db()


app.include_router(files_router)
app.include_router(stages_router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}

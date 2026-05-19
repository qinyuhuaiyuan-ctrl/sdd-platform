from fastapi import FastAPI
from database import init_db
from routers.files import router as files_router
from routers.git import router as git_router
from routers.stages import router as stages_router
from routers.skills import router as skills_router
from routers.templates import router as templates_router

app = FastAPI(title="SDD Platform")


@app.on_event("startup")
async def startup():
    await init_db()


app.include_router(files_router)
app.include_router(git_router)
app.include_router(stages_router)
app.include_router(skills_router)
app.include_router(templates_router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}

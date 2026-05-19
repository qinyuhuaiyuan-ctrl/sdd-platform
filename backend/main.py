import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from database import init_db
from routers.files import router as files_router
from routers.git import router as git_router
from routers.stages import router as stages_router
from routers.skills import router as skills_router
from routers.templates import router as templates_router
from services.terminal_service import TerminalSession, set_terminal

app = FastAPI(title="SDD Platform")

terminal_session = TerminalSession()


@app.on_event("startup")
async def startup():
    await init_db()


app.include_router(files_router)
app.include_router(git_router)
app.include_router(stages_router)
app.include_router(skills_router)
app.include_router(templates_router)


@app.websocket("/api/terminal")
async def terminal_ws(ws: WebSocket):
    global terminal_session
    await ws.accept()

    if terminal_session.process is None:
        terminal_session.start()
        set_terminal(terminal_session)

    # Auto-inject current stage skill on connect
    from services.stage_service import get_stages

    stages = await get_stages()
    active = next(s for s in stages["stages"] if s["status"] == "active")
    skill_name = active["skill_file"].split("/")[-2]
    terminal_session.inject_command(f"/{skill_name}")

    async def handle_incoming():
        while True:
            try:
                data = await ws.receive_text()
                if data.startswith('{"cols":'):
                    import json

                    info = json.loads(data)
                    terminal_session.resize(
                        info.get("rows", 24), info.get("cols", 80)
                    )
                else:
                    terminal_session.write(data)
            except WebSocketDisconnect:
                break
            except Exception:
                break

    await asyncio.gather(handle_incoming(), terminal_session.stream_to_ws(ws))


@app.get("/api/health")
async def health():
    return {"status": "ok"}

from fastapi import APIRouter, HTTPException
from config import PROJECT_REPO_PATH
from models import StagesResponse, AdvanceStageResponse
from services.stage_service import get_stages, advance_stage
from services.terminal_service import get_terminal

router = APIRouter(prefix="/api/stages", tags=["stages"])


@router.get("")
async def list_stages() -> StagesResponse:
    result = await get_stages()
    return StagesResponse(**result)


@router.post("/next")
async def next_stage() -> AdvanceStageResponse:
    try:
        result = await advance_stage(PROJECT_REPO_PATH)
        terminal = get_terminal()
        if terminal:
            terminal.inject_command(result["skill_command"])
        return AdvanceStageResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

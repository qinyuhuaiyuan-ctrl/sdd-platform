# backend/services/stage_service.py
from datetime import datetime, timezone
from pathlib import Path
from database import get_db
from services.git_service import git_log


async def get_stages() -> dict:
    db = await get_db()
    cursor = await db.execute('''
        SELECT s.id, s.name, s.display_order, s.skill_file,
               ps.status, ps.started_at, ps.completed_at
        FROM stages s
        JOIN project_stages ps ON s.id = ps.stage_id
        ORDER BY s.display_order
    ''')
    rows = await cursor.fetchall()
    await db.close()

    stages = []
    current = None
    for row in rows:
        stage = {
            "id": row[0], "name": row[1], "display_order": row[2],
            "skill_file": row[3], "status": row[4],
            "started_at": row[5], "completed_at": row[6]
        }
        stages.append(stage)
        if row[4] == "active":
            current = row[1]

    return {"stages": stages, "current_stage": current}


async def advance_stage(repo_path: Path) -> dict:
    stages = await get_stages()
    active = next(s for s in stages["stages"] if s["status"] == "active")
    current_name = active["name"]

    # 校验产出物
    if current_name == "brainstorming":
        spec = repo_path / ".sdd" / "spec.md"
        if not spec.exists() or len(spec.read_text().strip()) == 0:
            raise ValueError("spec.md 不存在或为空，请先在终端中完成 brainstorming")

    elif current_name == "plan":
        plan = repo_path / ".sdd" / "plan.md"
        if not plan.exists() or len(plan.read_text().strip()) == 0:
            raise ValueError("plan.md 不存在或为空，请先在终端中完成 plan")

    elif current_name == "implement":
        commits = git_log(repo_path)
        if len(commits) == 0:
            raise ValueError("尚未提交任何 commit，请先在终端中完成编码")

    elif current_name == "complete":
        raise ValueError("已是最终阶段，无法继续推进")

    db = await get_db()

    # 当前阶段标记完成
    now = datetime.now(timezone.utc).isoformat()
    await db.execute(
        "UPDATE project_stages SET status = 'completed', completed_at = ? WHERE stage_id = ?",
        (now, active["id"])
    )

    # 下一阶段激活
    next_order = active["display_order"] + 1
    cursor = await db.execute(
        "SELECT id, name, skill_file FROM stages WHERE display_order = ?", (next_order,)
    )
    next_row = await cursor.fetchone()
    await db.execute(
        "UPDATE project_stages SET status = 'active', started_at = ? WHERE stage_id = ?",
        (now, next_row[0])
    )

    await db.commit()
    await db.close()

    skill_name = next_row[2].split('/')[-2]
    skill_command = f"/{skill_name}"

    return {
        "from_stage": current_name,
        "to_stage": next_row[1],
        "skill_command": skill_command
    }

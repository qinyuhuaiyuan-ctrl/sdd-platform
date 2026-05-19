# backend/scripts/import_skills.py
import shutil
from pathlib import Path
from config import SKILLS_DIR, TEMPLATES_DIR

SUPERPOWERS_SKILLS = Path.home() / ".claude/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills"

SKILL_MAP = {
    "brainstorming": "brainstorming",
    "writing-plans": "writing-plans",
    "subagent-driven-development": "subagent-driven-development",
    "finishing-a-development-branch": "finishing-a-development-branch",
}

def import_skills():
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    for src_name, dst_name in SKILL_MAP.items():
        src = SUPERPOWERS_SKILLS / src_name
        dst = SKILLS_DIR / dst_name
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"Imported: {dst_name}")

def init_templates():
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

    spec_template = TEMPLATES_DIR / "spec-template.md"
    if not spec_template.exists():
        spec_template.write_text("""# 需求规格

## 架构 Architecture
<!-- 系统整体架构描述 -->

## 组件 Components
<!-- 各组件及其职责 -->

## 数据流 Data Flow
<!-- 数据如何流转 -->

## 错误处理 Error Handling
<!-- 错误场景和处理策略 -->

## 测试 Testing
<!-- 测试策略和验收标准 -->
""")

    plan_template = TEMPLATES_DIR / "plan-template.md"
    if not plan_template.exists():
        plan_template.write_text("""# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development

**Goal:** [一句话描述]

**Architecture:** [2-3句架构说明]

**Tech Stack:** [关键技术栈]

---

### Task N: [Component Name]

**Files:**
- Create: `path/to/file.py`
- Modify: `path/to/existing.py`

- [ ] **Step 1: Write the failing test**
- [ ] **Step 2: Run test to verify it fails**
- [ ] **Step 3: Write minimal implementation**
- [ ] **Step 4: Run test to verify it passes**
- [ ] **Step 5: Commit**
""")

if __name__ == "__main__":
    import_skills()
    init_templates()
    print("Done.")

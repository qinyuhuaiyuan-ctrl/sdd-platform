from pathlib import Path

def read_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding="utf-8")

def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def scan_file_tree(root: Path) -> list[dict]:
    items = []
    for p in sorted(root.iterdir()):
        if p.name.startswith('.git') or p.name == '__pycache__':
            continue
        if p.is_dir():
            items.append({
                "name": p.name,
                "type": "directory",
                "children": scan_file_tree(p)
            })
        else:
            items.append({
                "name": p.name,
                "type": "file",
                "path": str(p.relative_to(root))
            })
    return items

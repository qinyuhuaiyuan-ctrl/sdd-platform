# backend/test_file_service.py
import pytest
import tempfile
from pathlib import Path
from services.file_service import read_file, write_file, scan_file_tree

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)

def test_read_write_file(temp_dir):
    f = temp_dir / "test.md"
    write_file(f, "# Hello")
    assert read_file(f) == "# Hello"

def test_read_nonexistent_file(temp_dir):
    with pytest.raises(FileNotFoundError):
        read_file(temp_dir / "nope.md")

def test_scan_file_tree(temp_dir):
    (temp_dir / "a.md").write_text("a")
    (temp_dir / "sub").mkdir()
    (temp_dir / "sub" / "b.py").write_text("b")
    tree = scan_file_tree(temp_dir)
    names = [item["name"] for item in tree]
    assert "a.md" in names
    assert "sub" in names

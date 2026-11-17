"""Syntax and structure validation for the four Colab notebooks."""
from pathlib import Path
import ast
import json

root = Path(__file__).resolve().parent
notebooks = sorted(root.rglob("*.ipynb"))
assert len(notebooks) == 4, f"Expected 4 notebooks; found {len(notebooks)}"
for path in notebooks:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4
    code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
    assert code_cells, f"No code cells in {path}"
    for index, cell in enumerate(code_cells):
        source = cell["source"]
        script = "".join(source) if isinstance(source, list) else source
        try:
            ast.parse(script, filename=str(path))
        except SyntaxError as exc:
            raise SyntaxError(f"Code cell {index+1} in {path}: {exc}") from exc
    print(f"OK: {path.relative_to(root)} ({len(code_cells)} Python cells)")

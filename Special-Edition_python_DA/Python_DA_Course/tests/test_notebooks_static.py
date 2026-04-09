"""Static smoke tests for Python_DA_Course notebooks.

Stdlib-only: works without numpy/pandas/jupyter/nbformat installed.
Run:
    python -m pytest tests/
    python tests/test_notebooks_static.py
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

try:
    import pytest
except ImportError:  # pragma: no cover
    pytest = None  # type: ignore

COURSE_ROOT = Path(__file__).resolve().parent.parent
DATASETS_DIR = COURSE_ROOT / "datasets" / "ecommerce"

NOTEBOOKS = [
    "M1_Numpy_Basic/S1_numpy_vectorization.ipynb",
    "M2_Pandas_Basic/S2_pandas_io_cleaning.ipynb",
    "M3_Pandas_Advanced/S3_pandas_transform.ipynb",
    "M3_Pandas_Advanced/S4_timeseries_eda.ipynb",
    "M4_Matplotlib_Seaborn_Basic/S5_visualization_essentials.ipynb",
    "M6_Plotly_Projects/S6_plotly_capstone.ipynb",
]


def _load_notebook(rel_path: str) -> dict:
    nb_path = COURSE_ROOT / rel_path
    assert nb_path.exists(), f"Notebook not found: {nb_path}"
    with nb_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _concat_code_cells(nb: dict) -> str:
    chunks = []
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        src = cell.get("source", "")
        if isinstance(src, list):
            src = "".join(src)
        # Strip IPython magics / shell lines that break ast.parse
        cleaned = "\n".join(
            line for line in src.splitlines()
            if not line.lstrip().startswith(("%", "!", "?"))
        )
        chunks.append(cleaned)
    return "\n\n".join(chunks)


if pytest is not None:

    @pytest.mark.parametrize("rel_path", NOTEBOOKS)
    def test_notebook_is_valid_json(rel_path: str) -> None:
        nb = _load_notebook(rel_path)
        assert "cells" in nb, f"{rel_path} missing 'cells' key"
        assert isinstance(nb["cells"], list)

    @pytest.mark.parametrize("rel_path", NOTEBOOKS)
    def test_notebook_code_cells_parse(rel_path: str) -> None:
        nb = _load_notebook(rel_path)
        code = _concat_code_cells(nb)
        try:
            ast.parse(code)
        except SyntaxError as exc:
            raise AssertionError(f"Syntax error in {rel_path}: {exc}") from exc

    @pytest.mark.parametrize("rel_path", NOTEBOOKS)
    def test_notebook_has_expected_structure(rel_path: str) -> None:
        nb = _load_notebook(rel_path)
        types = [c.get("cell_type") for c in nb.get("cells", [])]
        assert types.count("markdown") >= 1, f"{rel_path} has no markdown cell"
        assert types.count("code") >= 1, f"{rel_path} has no code cell"

    def test_datasets_exist() -> None:
        required = ["products.csv", "orders_raw.csv", "customers.csv"]
        missing = [name for name in required if not (DATASETS_DIR / name).exists()]
        assert not missing, f"Missing datasets under {DATASETS_DIR}: {missing}"

    def test_readme_mentions_all_sessions() -> None:
        readme = COURSE_ROOT / "README.md"
        assert readme.exists(), f"README.md not found at {readme}"
        text = readme.read_text(encoding="utf-8")
        missing = [f"S{i}" for i in range(1, 7) if f"S{i}" not in text]
        assert not missing, f"README.md missing session markers: {missing}"


if __name__ == "__main__":
    if pytest is None:
        print("pytest not installed — install via: pip install pytest")
        raise SystemExit(1)
    raise SystemExit(pytest.main([__file__, "-v"]))

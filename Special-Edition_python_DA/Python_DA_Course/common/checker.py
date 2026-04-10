"""大地遊戲 — 答對就告訴你解答在哪。"""
from __future__ import annotations

import hashlib

# (session, salt, expected_hash, answer_type)
_ANSWERS: dict[str, tuple[str, str, str]] = {
    "S1": ("a1b2", "", "scalar_float"),
    "S2": ("c3d4", "", "scalar_int"),
    "S3": ("e5f6", "", "string"),
    "S4": ("g7h8", "", "scalar_int"),
    "S5": ("i9j0", "", "string"),
}


def _hash(value: str, salt: str) -> str:
    return hashlib.sha256(f"{salt}:{value}".encode()).hexdigest()


def _canon(answer, atype: str) -> str:
    if atype == "scalar_float":
        return f"{float(answer):.1f}"
    if atype == "scalar_int":
        return str(int(round(float(answer))))
    if atype == "shape":
        if hasattr(answer, "__iter__") and not isinstance(answer, str):
            return str(tuple(int(x) for x in answer))
        return str(answer).strip()
    return str(answer).strip()


def _build_answers() -> None:
    """One-time: compute hashes (called at import)."""
    raw = {
        "S1": ("a1b2", "27153.1", "scalar_float"),
        "S2": ("c3d4", "188",     "scalar_int"),
        "S3": ("e5f6", "Books",   "string"),
        "S4": ("g7h8", "186506",  "scalar_int"),
        "S5": ("i9j0", "North",   "string"),
    }
    for k, (salt, val, atype) in raw.items():
        _ANSWERS[k] = (salt, _hash(val, salt), atype)


_build_answers()


def check(session: str, answer) -> None:
    """答對就告訴你解答放在哪。"""
    session = session.upper()
    if session not in _ANSWERS:
        print(f"❓ 未知的關卡: {session}")
        return

    salt, expected, atype = _ANSWERS[session]
    canonical = _canon(answer, atype)

    if _hash(canonical, salt) == expected:
        n = session.replace("S", "")
        path = f"docs/_archive/S{n}_ref.ipynb"
        print(f"🎉 答對了！解答在這裡 → 📂 {path}")
    else:
        print("❌ 再想想，答案不對喔！")

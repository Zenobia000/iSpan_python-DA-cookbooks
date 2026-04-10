"""大地遊戲 — 答對就告訴你解答在哪。"""
from __future__ import annotations

import hashlib

# (salt, sha256_hash, answer_type) — 答案只存 hash，看原始碼也看不到
_ANSWERS: dict[str, tuple[str, str, str]] = {
    "S1": ("b82eb58cf00db96b", "86a13e8199f205aefb8fb888b51b5c3eacdbf131ea3c458b9031b2419914ab1f", "scalar_float"),
    "S2": ("55aa04661f1ae01d", "65b01ebc23c05634e7b2d860f6419f1315ca11805c6f6b6aac69898a19e81efd", "scalar_int"),
    "S3": ("050128305c0a6cc3", "946807bb0f40474aeb185efb777fa18e886037dc5d2ae664c36b4ce7f112c72e", "string"),
    "S4": ("89c39799a0bb306c", "8df8c66eb0b301bcceb00afe9114448feb9a4a1634e0e265818538b8dbdd51f8", "scalar_int"),
    "S5": ("99e8a10951b402ef", "2ac15345b19fdcc550ad2a54516321f0933a2d61b50f1d4b74c51f584814831b", "string"),
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

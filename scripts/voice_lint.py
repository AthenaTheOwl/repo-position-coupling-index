from __future__ import annotations

from pathlib import Path

FORBIDDEN_WORDS = {
    "synergy",
    "synergistic",
    "strategic",
    "game-changing",
    "revolutionary",
    "transformative",
}

FORBIDDEN_PHRASES = {
    "not just",
    "not only",
    "more than",
}


def main() -> int:
    failures: list[str] = []
    for path in sorted(Path("coupling_index").glob("*.md")):
        text = path.read_text(encoding="utf-8").lower()
        for word in sorted(FORBIDDEN_WORDS):
            if word in text:
                failures.append(f"{path}: forbidden word `{word}`")
        for phrase in sorted(FORBIDDEN_PHRASES):
            if phrase in text:
                failures.append(f"{path}: forbidden phrase `{phrase}`")

    if failures:
        print("\n".join(failures))
        return 1
    print("voice lint ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


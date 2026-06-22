from __future__ import annotations

import re
from pathlib import Path

REF_RE = re.compile(r"R-RPC-\d{3}")


def main() -> int:
    specs_dir = Path("specs")
    defined: set[str] = set()
    referenced: dict[str, set[str]] = {}

    for requirements in specs_dir.glob("*/requirements.md"):
        defined.update(REF_RE.findall(requirements.read_text(encoding="utf-8")))

    for path in sorted(specs_dir.glob("*/*.md")):
        if path.name == "requirements.md":
            continue
        refs = set(REF_RE.findall(path.read_text(encoding="utf-8")))
        if refs:
            referenced[str(path)] = refs

    missing: list[str] = []
    for path, refs in referenced.items():
        for ref in sorted(refs - defined):
            missing.append(f"{path}: {ref} is referenced but not defined")

    if missing:
        print("\n".join(missing))
        return 1
    print(f"spec check ok: {len(defined)} requirements defined")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


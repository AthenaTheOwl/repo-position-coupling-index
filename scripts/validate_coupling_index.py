from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from repo_position_coupling_index.frontmatter import load_index  # noqa: E402
from repo_position_coupling_index.scoring import compute_flags  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    paths = [Path(arg) for arg in args] if args else default_paths()
    if not paths:
        print("no coupling index files found")
        return 1

    failures: list[str] = []
    for path in paths:
        try:
            index = load_index(path)
            expected = [flag.model_dump(mode="json", exclude_none=True) for flag in compute_flags(index)]
            actual = index.as_plain_data()["flagged"]
            if actual != expected:
                failures.append(f"{path}: flagged section differs from computed flags")
        except Exception as exc:  # noqa: BLE001 - gate prints all validation failures.
            failures.append(f"{path}: {exc}")

    if failures:
        print("\n".join(failures))
        return 1
    print(f"validated {len(paths)} coupling index file(s)")
    return 0


def default_paths() -> list[Path]:
    return sorted(Path("coupling_index").glob("*.md")) + sorted(Path("examples").glob("*.md"))


if __name__ == "__main__":
    raise SystemExit(main())

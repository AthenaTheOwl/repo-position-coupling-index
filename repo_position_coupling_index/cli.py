from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from repo_position_coupling_index.diff import render_diff
from repo_position_coupling_index.frontmatter import load_index
from repo_position_coupling_index.model import CouplingIndex
from repo_position_coupling_index.render import render_index
from repo_position_coupling_index.scoring import with_computed_flags


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="coupling")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="validate one report")
    validate.add_argument("path")
    validate.set_defaults(func=cmd_validate)

    render = subparsers.add_parser("render", help="render a report from front matter")
    render.add_argument("path")
    render.add_argument("--write", action="store_true", help="rewrite the file in place")
    render.set_defaults(func=cmd_render)

    flag = subparsers.add_parser("flag", help="compute flags for a report month")
    flag.add_argument("--month", required=True)
    flag.add_argument("--index-dir", default="coupling_index")
    flag.add_argument("--check", action="store_true", help="fail if computed flags differ")
    flag.set_defaults(func=cmd_flag)

    diff = subparsers.add_parser("diff", help="diff two report months")
    diff.add_argument("--from", dest="from_month", required=True)
    diff.add_argument("--to", dest="to_month", required=True)
    diff.add_argument("--index-dir", default="coupling_index")
    diff.set_defaults(func=cmd_diff)

    new = subparsers.add_parser("new", help="create a report from a prior report")
    new.add_argument("--month", required=True)
    new.add_argument("--from-month")
    new.add_argument("--index-dir", default="coupling_index")
    new.set_defaults(func=cmd_new)

    return parser


def cmd_validate(args: argparse.Namespace) -> int:
    index = load_index(args.path)
    print(f"validated {args.path}: {len(index.couplings)} couplings, {len(index.flagged)} flags")
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    path = Path(args.path)
    index = load_index(path)
    rendered = render_index(index)
    if args.write:
        path.write_text(rendered, encoding="utf-8")
        print(f"rendered {path}")
    else:
        print(rendered, end="")
    return 0


def cmd_flag(args: argparse.Namespace) -> int:
    path = resolve_month(args.month, Path(args.index_dir))
    index = load_index(path)
    updated = with_computed_flags(index)
    if args.check:
        if index.as_plain_data()["flagged"] != updated.as_plain_data()["flagged"]:
            print(f"flag drift in {path}")
            return 1
        print(f"flags ok {path}: {len(index.flagged)}")
        return 0

    path.write_text(render_index(updated), encoding="utf-8")
    print(f"flagged {path}: {len(updated.flagged)}")
    return 0


def cmd_diff(args: argparse.Namespace) -> int:
    previous = load_index(resolve_month(args.from_month, Path(args.index_dir)))
    current = load_index(resolve_month(args.to_month, Path(args.index_dir)))
    print(render_diff(previous, current), end="")
    return 0


def cmd_new(args: argparse.Namespace) -> int:
    index_dir = Path(args.index_dir)
    index_dir.mkdir(parents=True, exist_ok=True)
    target = index_dir / f"{args.month}.md"
    if target.exists():
        raise SystemExit(f"report already exists: {target}")

    source_month = args.from_month or latest_month(index_dir)
    source = load_index(resolve_month(source_month, index_dir))
    data = source.as_plain_data()
    data["month"] = args.month
    data["flagged"] = []
    created = CouplingIndex.model_validate(data)
    target.write_text(render_index(created), encoding="utf-8")
    print(f"created {target}")
    return 0


def resolve_month(month_or_path: str, index_dir: Path) -> Path:
    path = Path(month_or_path)
    if path.suffix == ".md" and path.exists():
        return path
    if path.exists():
        return path

    candidates = [
        index_dir / f"{month_or_path}.md",
        Path("examples") / f"{month_or_path}.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise SystemExit(f"report not found for month: {month_or_path}")


def latest_month(index_dir: Path) -> str:
    reports = sorted(index_dir.glob("*.md"))
    if not reports:
        raise SystemExit("no prior reports found; pass --from-month")
    return reports[-1].stem


if __name__ == "__main__":
    raise SystemExit(main())

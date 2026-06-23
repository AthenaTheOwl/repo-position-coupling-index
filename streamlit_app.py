from __future__ import annotations

from pathlib import Path

import streamlit as st

from pydantic import ValidationError

from repo_position_coupling_index.frontmatter import load_index
from repo_position_coupling_index.model import CouplingIndex
from repo_position_coupling_index.scoring import compute_flags
from repo_position_coupling_index.show import headline, rank_pillars

REPORT = Path(__file__).resolve().parent / "coupling_index" / "2026-M07.md"

st.set_page_config(page_title="repo position coupling index", layout="wide")

st.title("repo position coupling index")
st.caption(
    "monthly index linking repo-portfolio slugs to investing thesis-pillar ids. "
    "ranks pillars by live build exposure and lists the open flags that need a decision."
)

if not REPORT.exists():
    st.warning(f"committed report not found at {REPORT}. nothing to show.")
    st.stop()

index = load_index(REPORT)
ranked = rank_pillars(index)

col1, col2, col3 = st.columns(3)
col1.metric("couplings", len(index.couplings))
col2.metric("pillars tracked", len(index.pillar_states))
col3.metric("open flags", len(index.flagged))

st.info(headline(index, ranked))

verdicts = sorted({str(r["verdict"]) for r in ranked})
chosen = st.multiselect(
    "filter pillars by verdict",
    options=verdicts,
    default=verdicts,
    help="narrow the ranking to specific pillar verdicts",
)

st.subheader("pillars by live build exposure")
rows = [
    {
        "pillar": str(r["pillar_id"]),
        "verdict": str(r["verdict"]),
        "repos": int(r["repos"]),
        "exposure": int(r["exposure"]),
    }
    for r in ranked
    if str(r["verdict"]) in chosen
]
if rows:
    st.dataframe(rows, use_container_width=True, hide_index=True)
else:
    st.write("no pillars match the selected verdicts.")

st.subheader("open flags")
flag_rows = [
    {
        "flag": f.flag,
        "repo": f.repo_slug or "-",
        "pillar": f.pillar_id or "-",
        "reason": f.reason,
        "prompt": f.prompt,
    }
    for f in index.flagged
]
if flag_rows:
    st.dataframe(flag_rows, use_container_width=True, hide_index=True)
else:
    st.write("no open flags.")

st.caption(f"source: {REPORT.name} (read-only, offline)")

# ---------------------------------------------------------------------------
# interactive: drive the real engine on your own coupling graph
# ---------------------------------------------------------------------------
st.divider()
st.header("re-couple it yourself")
st.caption(
    "edit the live state below — flip a repo to dead, change a pillar verdict, "
    "add or re-direct a coupling — and the app re-runs the real engine "
    "(rank_pillars + compute_flags) on your graph. nothing is hardcoded: the "
    "ranking and the open flags are recomputed live from your edits."
)

REPO_STATUSES = ["alive", "quiet", "dead"]
VERDICTS = ["confirming", "weakening", "invalidated"]
DIRECTIONS = ["bets-on", "bets-against", "hedged", "orphan"]
CONFIDENCES = ["low", "medium", "high"]

# seed the editors from the committed index so the user starts from a real graph.
seed_repos = [{"repo_slug": s.repo_slug, "alive_status": s.alive_status} for s in index.repo_states]
seed_pillars = [
    {"pillar_id": s.pillar_id, "current_verdict": s.current_verdict} for s in index.pillar_states
]
seed_couplings = [
    {
        "repo_slug": c.repo_slug,
        "pillar_id": c.pillar_id,
        "direction": c.direction,
        "mechanism": c.mechanism,
        "confidence": c.confidence,
        "created_month": c.created_month,
    }
    for c in index.couplings
]

st.subheader("repo states")
st.caption("alive repos add live build exposure; dead repos can fire re-examine flags.")
edited_repos = st.data_editor(
    seed_repos,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={
        "repo_slug": st.column_config.TextColumn("repo_slug", required=True),
        "alive_status": st.column_config.SelectboxColumn(
            "alive_status", options=REPO_STATUSES, required=True
        ),
    },
    key="repo_editor",
)

st.subheader("pillar states")
st.caption("an alive repo coupled to an invalidated pillar fires a re-thesis flag.")
edited_pillars = st.data_editor(
    seed_pillars,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={
        "pillar_id": st.column_config.TextColumn("pillar_id", required=True),
        "current_verdict": st.column_config.SelectboxColumn(
            "current_verdict", options=VERDICTS, required=True
        ),
    },
    key="pillar_editor",
)

st.subheader("couplings")
st.caption(
    "each row is a repo betting on / against / hedging a pillar. orphan = no real link. "
    "mechanism must be 1-3 sentences (model rule)."
)
edited_couplings = st.data_editor(
    seed_couplings,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    column_config={
        "repo_slug": st.column_config.TextColumn("repo_slug", required=True),
        "pillar_id": st.column_config.TextColumn("pillar_id", required=True),
        "direction": st.column_config.SelectboxColumn(
            "direction", options=DIRECTIONS, required=True
        ),
        "mechanism": st.column_config.TextColumn("mechanism", width="large", required=True),
        "confidence": st.column_config.SelectboxColumn(
            "confidence", options=CONFIDENCES, required=True
        ),
        "created_month": st.column_config.TextColumn("created_month", required=True),
    },
    key="coupling_editor",
)


def _clean(rows: list[dict]) -> list[dict]:
    """drop fully-empty editor rows that streamlit leaves behind."""
    out = []
    for row in rows:
        if any((str(v).strip() if v is not None else "") for v in row.values()):
            out.append({k: (v if v is not None else "") for k, v in row.items()})
    return out


if st.button("recompute with the real engine", type="primary"):
    payload = {
        "month": index.month,
        "repo_states": _clean(edited_repos),
        "pillar_states": _clean(edited_pillars),
        "couplings": _clean(edited_couplings),
        "flagged": [],  # engine derives these; we ignore any committed ones here
    }
    try:
        # CouplingIndex re-runs the REAL validators (patterns, sentence count,
        # known-node references); compute_flags + rank_pillars are the REAL engine.
        live_index = CouplingIndex.model_validate(payload)
    except ValidationError as exc:
        st.error("your graph did not validate — fix the rows below, then recompute.")
        for err in exc.errors():
            loc = " / ".join(str(p) for p in err["loc"])
            st.write(f"- `{loc}`: {err['msg']}")
    else:
        live_flags = compute_flags(live_index)
        live_ranked = rank_pillars(live_index)

        st.success("validated and recomputed on your graph.")
        st.info(headline(live_index, live_ranked))

        m1, m2, m3 = st.columns(3)
        m1.metric("couplings", len(live_index.couplings))
        m2.metric("pillars tracked", len(live_index.pillar_states))
        m3.metric("flags fired", len(live_flags))

        st.subheader("your pillars by live build exposure")
        st.dataframe(
            [
                {
                    "pillar": str(r["pillar_id"]),
                    "verdict": str(r["verdict"]),
                    "repos": int(r["repos"]),
                    "exposure": int(r["exposure"]),
                }
                for r in live_ranked
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("flags the engine fired on your graph")
        if live_flags:
            st.dataframe(
                [
                    {
                        "flag": f.flag,
                        "repo": f.repo_slug or "-",
                        "pillar": f.pillar_id or "-",
                        "reason": f.reason,
                        "prompt": f.prompt,
                    }
                    for f in live_flags
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.write("no flags fired — every repo is coupled and no thesis/hedge conflict.")
else:
    st.caption(
        "edit any table, then press the button to run the real engine. "
        "try: set a repo to `dead` whose pillar is `confirming`, or flip a pillar to "
        "`invalidated` while its repo stays `alive` — watch the flags change."
    )

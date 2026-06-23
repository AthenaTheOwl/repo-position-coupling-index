from __future__ import annotations

from pathlib import Path

import streamlit as st

from repo_position_coupling_index.frontmatter import load_index
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

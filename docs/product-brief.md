# Product Brief

## Purpose

Repo Position Coupling Index keeps one monthly Markdown report that links two
manual registries:

- repos the user is building or maintaining
- thesis pillars the user tracks in the investing process

The output is an edge list between repo slugs and pillar ids. Each edge names a
shared causal mechanism and a direction. The report also lists flags that ask
for a concrete review action.

## User

The user already keeps repo-level theses and pillar-level verdicts. This repo
does not replace those sources. It shows where the two sources imply the same
bet, where they diverge, and where one side has no counterpart.

## v0.1 behavior

- Validate monthly report front matter.
- Render report front matter back to Markdown.
- Compute five flag types from repo state, pillar state, and coupling rows.
- Diff two monthly reports for added, removed, and direction-changed couplings.
- Keep the report body readable enough for review in git.

## Non-goals

- No causal scoring.
- No GitHub activity crawl.
- No auto-import from the pillar tracker.
- No multi-user workflow.


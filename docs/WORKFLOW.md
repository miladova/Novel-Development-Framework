# Author-governed workflow

`Intake → Dry inspection → Author approves preservation → Immutable archive → Source mapping → Atomic staging → Review queue → Author decision → Canon promotion → Story design → Writing brief → Author prose approval → Draft → Continuity and voice QA → Publication authorization`

Every arrow is a gate, not a background automation. Use separate commits for distinct phases.

## Review stops
Stop when transcript completeness, speaker attribution, file identity, event order, character identity, source authority, duplicate content, contradictions or approval are unclear. Record the blocker in `knowledge/review_queue/` instead of guessing.

## Series boundary
A single fictional universe may share one canonical knowledge base with per-book folders. Unrelated universes require separate repositories. A series cross-book assertion needs its own canonical source and should not be independently rewritten in each book.

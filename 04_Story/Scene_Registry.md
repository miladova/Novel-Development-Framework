# Scene registry guide

[Scene_Registry.csv](Scene_Registry.csv) is the single machine-readable registry. Keep one row per stable SCN ID and use the [scene template](../09_Tools/Templates/Scene.md) for detail.

Columns: scene_id, book_id, chapter, pov, purpose, change, status, depends_on, source_refs. Separate dependency IDs with semicolons and quote any CSV value containing commas. Every book_id refers to an existing `05_Books/BOOK-###/` folder.

Statuses: Planned, Drafting, Drafted, Reviewed, Approved, Released. Approval means accepted scene work, not canon promotion. Release requires its own authorization. Use purpose and change to show what the scene contributes rather than merely listing events.

The validator checks IDs, supported statuses, book folders, and whether named dependencies exist. It does not decide narrative order, evaluate pacing, or detect every logical dependency problem.

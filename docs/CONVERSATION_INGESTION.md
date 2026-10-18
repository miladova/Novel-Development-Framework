# Conversation intake and preservation

This framework does not ship an automatic conversation importer or semantic extractor.

Place an unchanged export in `_inbox/conversations/new/`. Its presence does not authorize reading or processing it. On a named, authorized inspection, report file type, speaker attribution, ordering, attachments, completeness, known gaps, and proposed handling. Do not reconstruct absent wording.

After separate preservation approval, copy the unchanged source into `archive/conversations/<source-ID>/original/`. Record filename, byte size, SHA-256, import time, authorization evidence, and known limitations. `python scripts/source_manifest.py "path/to/source"` can print a checksum report for one authorized file; it does not perform the copy.

Create a normalized transcript and stable message anchors only with verified source mapping. Preserve originals. Corrections belong in `supplements/`, and incomplete captures must be labeled incomplete or unknown.

Later, separately authorized extraction may create atomic claims in `knowledge/staging/`. Each claim cites the source and message anchor, identifies its speaker and status, and links related records. Create a specific review queue for uncertainty rather than repeating unsupported text across folders.

No intake or extraction step automatically updates canon, rewrites a manuscript, or publishes material. See [canon approval](CANON_APPROVAL_PROCESS.md) and [privacy](PRIVACY.md).

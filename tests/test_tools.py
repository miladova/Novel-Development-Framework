"""Behavioral tests for the optional local tools; all writing happens in temp dirs."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
HEADER = 'scene_id,book_id,chapter,pov,purpose,change,status,depends_on,source_refs\n'


def tool(name, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / name), *map(str, args)],
                          capture_output=True, text=True)


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for file in ROOT.rglob('*'):
            rel = file.relative_to(ROOT)
            if file.is_file() and not any(p in {'.git', '__pycache__', '_private'} for p in rel.parts):
                target = self.root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(file.read_bytes())

    def validate(self):
        return tool('validate_framework.py', '--root', self.root)

    def test_public_template_is_valid(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_validator_catches_missing_required_file(self):
        (self.root / 'AGENTS.md').unlink()
        self.assertNotEqual(self.validate().returncode, 0)

    def test_validator_catches_broken_relative_link(self):
        (self.root / 'README.md').write_text('# Title\n[Broken](missing.md)\n')
        result = self.validate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('missing.md', result.stdout)

    def test_validator_ignores_example_links_in_code(self):
        with (self.root / 'README.md').open('a') as f:
            f.write('\n```markdown\n[Example](not-a-file.md)\n```\n')
        self.assertEqual(self.validate().returncode, 0)

    def test_validator_rejects_outside_link(self):
        with (self.root / 'README.md').open('a') as f:
            f.write('\n[Outside](../outside.md)\n')
        self.assertNotEqual(self.validate().returncode, 0)

    def test_validator_does_not_read_inbox_content(self):
        (self.root / '_inbox/manuscripts/unknown.md').write_bytes(b'\xff\xfe')
        self.assertEqual(self.validate().returncode, 0)

    def test_canon_template_is_not_preapproved(self):
        text = (self.root / '09_Tools/Templates/Canon_Record.md').read_text()
        self.assertIn('Status: Template', text)
        self.assertIn('Canonical: false', text)
        self.assertNotIn('Status: Canon\n', text)

    def test_canon_without_approval_is_rejected(self):
        p = self.root / '02_Canon/CAN-0001.md'
        p.write_text('---\nID: CAN-0001\nStatus: Canon\nCanonical: true\n---\n# Test record\n')
        result = self.validate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('approval', result.stdout.lower())

    def approved_canon_fixture(self):
        decision = self.root / '00_Project/DEC-0001.md'
        decision.write_text('---\nID: DEC-0001\nStatus: Approved\nApproved_By: Test author\nApproved_On: 2026-01-01\n---\n# Decision\n')
        source = self.root / '01_Artifacts/source.md'
        source.write_text('# Source\nExplicit author approval fixture.\n')
        canon = self.root / '02_Canon/CAN-0001.md'
        canon.write_text('---\nID: CAN-0001\nStatus: Canon\nCanonical: true\nApproved_By: Test author\nApproved_On: 2026-01-01\nSource: ../01_Artifacts/source.md\nDecision: ../00_Project/DEC-0001.md\n---\n# Record\n')
        return decision, canon

    def test_approved_canon_with_evidence_passes(self):
        self.approved_canon_fixture()
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_decision_requires_approval_date(self):
        decision, _ = self.approved_canon_fixture()
        decision.write_text(decision.read_text().replace('Approved_On: 2026-01-01\n', ''))
        self.assertNotEqual(self.validate().returncode, 0)

    def test_decision_cannot_point_into_an_inbox(self):
        decision, canon = self.approved_canon_fixture()
        inbox = self.root / '_inbox/manuscripts/decision.md'
        inbox.write_bytes(decision.read_bytes())
        canon.write_text(canon.read_text().replace('../00_Project/DEC-0001.md', '../_inbox/manuscripts/decision.md'))
        self.assertNotEqual(self.validate().returncode, 0)

    def test_duplicate_scene_id_is_rejected(self):
        (self.root / '05_Books/BOOK-001').mkdir()
        (self.root / '04_Story/Scene_Registry.csv').write_text(
            HEADER + 'SCN-0001,BOOK-001,1,,,,Planned,,\n' * 2)
        self.assertNotEqual(self.validate().returncode, 0)

    def test_invalid_scene_status_is_rejected(self):
        (self.root / '05_Books/BOOK-001').mkdir()
        (self.root / '04_Story/Scene_Registry.csv').write_text(
            HEADER + 'SCN-0001,BOOK-001,1,,,,Magic,,\n')
        self.assertNotEqual(self.validate().returncode, 0)

    def test_missing_dependency_is_rejected(self):
        (self.root / '05_Books/BOOK-001').mkdir()
        (self.root / '04_Story/Scene_Registry.csv').write_text(
            HEADER + 'SCN-0001,BOOK-001,1,,,,Planned,SCN-0002,\n')
        self.assertNotEqual(self.validate().returncode, 0)

    def test_book_creation_is_dry_run_by_default(self):
        result = tool('create_book.py', '--root', self.root, '--id', 'BOOK-001', '--title', 'Sample')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((self.root / '05_Books/BOOK-001').exists())

    def test_book_creation_requires_explicit_apply_and_keeps_title(self):
        result = tool('create_book.py', '--root', self.root, '--id', 'BOOK-001', '--title', 'Sample', '--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('Sample', (self.root / '05_Books/BOOK-001/README.md').read_text())
        self.assertEqual(self.validate().returncode, 0)

    def test_book_creation_never_overwrites(self):
        args = ('--root', self.root, '--id', 'BOOK-001', '--title', 'Sample', '--apply')
        created = tool('create_book.py', *args)
        self.assertEqual(created.returncode, 0, created.stderr)
        p = self.root / '05_Books/BOOK-001/README.md'
        p.write_text('keep me')
        self.assertNotEqual(tool('create_book.py', *args).returncode, 0)
        self.assertEqual(p.read_text(), 'keep me')

    def test_book_creation_rejects_traversal(self):
        result = tool('create_book.py', '--root', self.root, '--id', '../escape', '--title', 'Sample', '--apply')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.root / 'escape').exists())

    @unittest.skipIf(sys.platform == 'win32', 'Windows symlinks need additional privileges')
    def test_book_creation_rejects_symlink_template(self):
        p = self.root / '05_Books/BOOK_TEMPLATE/README.md'
        p.unlink()
        p.symlink_to(self.root / 'README.md')
        result = tool('create_book.py', '--root', self.root, '--id', 'BOOK-001', '--title', 'Sample', '--apply')
        self.assertNotEqual(result.returncode, 0)

    def test_status_does_not_read_manuscripts_unless_words_requested(self):
        book = self.root / '05_Books/BOOK-001/Chapters'
        book.mkdir(parents=True)
        (book / 'Chapter_01.md').write_bytes(b'\xff')
        result = tool('project_status.py', '--root', self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('not requested', result.stdout.lower())
        self.assertNotEqual(tool('project_status.py', '--root', self.root, '--words').returncode, 0)

    def test_status_counts_only_active_plain_text_chapters(self):
        book = self.root / '05_Books/BOOK-001/Chapters'
        book.mkdir(parents=True)
        (book / 'Chapter_01.md').write_text('one two three')
        (book / 'README.md').write_text('not manuscript prose')
        (book / 'old.docx').write_bytes(b'not a docx parser')
        result = tool('project_status.py', '--root', self.root, '--words')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('| BOOK-001 | 3 |', result.stdout)

    def test_manifest_hashes_exact_bytes_without_writing(self):
        source = self.root / '_inbox/manuscripts/source.txt'
        data = b'original\r\ntext\x00'
        source.write_bytes(data)
        before = set(self.root.rglob('*'))
        result = tool('source_manifest.py', source)
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = json.loads(result.stdout)
        self.assertEqual(manifest['sha256'], hashlib.sha256(data).hexdigest())
        self.assertEqual(manifest['bytes'], len(data))
        self.assertEqual(source.read_bytes(), data)
        self.assertEqual(set(self.root.rglob('*')), before)

    def test_manifest_rejects_missing_source(self):
        self.assertNotEqual(tool('source_manifest.py', self.root / 'absent.txt').returncode, 0)


if __name__ == '__main__':
    unittest.main()

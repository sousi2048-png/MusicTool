import runpy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class OutputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'original'
        self.source = self.root / 'Artist' / 'Album' / 'song.wav'
        self.source.parent.mkdir(parents=True)
        self.source.write_bytes(b'original')
        self.output = self.base / 'output'
        self.dest = self.output / self.source.relative_to(self.root)
        self.core = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'M_norm'))
        self.globals = self.core['main'].__globals__
        self.args = ['-o', str(self.output), '--log-file', str(self.base / 'log.md'), str(self.root)]

    def run_main(self, *extra, near=False, fail=False):
        stats = {'input_i': '-14' if near else '-8', 'input_tp': '-2'}
        def encode(ffmpeg, source, dest, *args):
            dest.write_bytes(b'normalized')
            if fail:
                raise RuntimeError('encoding failed')
        with patch.dict(self.globals, analysis_pass=lambda *a: stats, normalize_pass=encode):
            return self.core['main'](self.args + list(extra))

    def test_structure_original_and_existing_output(self):
        self.assertEqual(self.run_main(), 0)
        self.assertEqual(self.dest.read_bytes(), b'normalized')
        self.assertEqual(self.source.read_bytes(), b'original')
        self.dest.write_bytes(b'existing')
        self.assertEqual(self.run_main(), 0)
        self.assertEqual(self.dest.read_bytes(), b'existing')
        self.assertEqual(self.run_main('--overwrite'), 0)
        self.assertEqual(self.dest.read_bytes(), b'normalized')

    def test_near_target_copied_and_dry_run(self):
        self.assertEqual(self.run_main('--dry-run', near=True), 0)
        self.assertFalse(self.output.exists())
        self.assertFalse((self.base / 'log.md').exists())
        self.assertEqual(self.run_main(near=True), 0)
        self.assertEqual(self.dest.read_bytes(), b'original')

    def test_failed_overwrite_preserves_output(self):
        self.dest.parent.mkdir(parents=True)
        self.dest.write_bytes(b'existing')
        self.assertEqual(self.run_main('--overwrite', fail=True), 1)
        self.assertEqual(self.dest.read_bytes(), b'existing')
        self.assertEqual(self.source.read_bytes(), b'original')
        self.assertEqual(list(self.dest.parent.iterdir()), [self.dest])

    def test_overlap_and_symlink_escape_rejected(self):
        for output in (self.root, self.root / 'nested', self.base):
            self.assertEqual(self.core['main'](['-o', str(output), str(self.root)]), 1)
        self.output.mkdir()
        (self.output / 'Artist').symlink_to(self.root / 'Artist', target_is_directory=True)
        self.assertEqual(self.run_main('--overwrite'), 1)
        self.assertEqual(self.source.read_bytes(), b'original')


if __name__ == '__main__':
    unittest.main()

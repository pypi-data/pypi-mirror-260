import sys
import os.path
import io
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from renaming import command_line  # noqa: linter (pycodestyle) should not lint this line.


class test_renaming(unittest.TestCase):
    """command-line renaming unittest"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dry_run(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            command_line.main(["-d"])
            self.assertIn("[DRY-RUN]", fake_out.getvalue())
            command_line.main(["--dry-run"])
            self.assertIn("[DRY-RUN]", fake_out.getvalue())

    def test_config(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            command_line.main(["-c", "renaming.toml"])
            self.assertIn("renaming.toml", fake_out.getvalue())
            command_line.main(["--config", "renaming.toml"])
            self.assertIn("renaming.toml", fake_out.getvalue())

    def test_folder(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            command_line.main(["-f", "tests"])
            self.assertIn("tests", fake_out.getvalue())
            command_line.main(["--folder", "tests"])
            self.assertIn("tests", fake_out.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)

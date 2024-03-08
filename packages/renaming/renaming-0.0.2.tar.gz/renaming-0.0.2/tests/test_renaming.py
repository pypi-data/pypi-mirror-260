import sys
import os.path
import io
import unittest
from unittest.mock import patch

import consolecmdtools as cct

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import renaming  # noqa: linter (pycodestyle) should not lint this line.


class test_renaming(unittest.TestCase):
    """renaming unittest"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_version(self):
        self.assertIsInstance(renaming.__version__, str)

    def test_parse_config(self):
        folder = cct.get_path(__file__).parent
        config_path = os.path.join(folder, 'renaming.toml')
        self.assertEqual(renaming.parse_config(config_path, folder)['vars']['abbr'], 'TF')

    def test_validate_filename(self):
        self.assertTrue(renaming.validate_filename("test-2024", "test-\\d{4}"))

    def test_run_renaming(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            folder = cct.get_path(__file__).parent
            config_path = os.path.join(folder, 'renaming.toml')
            renaming.run_renaming(config_path=config_path, folder=folder, dry_run=True)
            self.assertIn("Renamed", fake_out.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)

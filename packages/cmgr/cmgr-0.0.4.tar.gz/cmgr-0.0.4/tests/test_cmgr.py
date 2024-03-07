import sys
import os.path
import io
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cmgr  # noqa: linter (pycodestyle) should not lint this line.


class test_cmgr(unittest.TestCase):
    """cmgr unittest"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_version(self):
        self.assertIsInstance(cmgr.__version__, str)

    def test_print_profile_help(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            cmgr.print_profile_help()
            self.assertIn('name =', fake_out.getvalue())

    def test_ensure_packages(self):
        with patch("sys.stdout", new=io.StringIO()) as fake_out:
            packages = [
                {
                    "name": "cmgr",
                    "cmd": "cmgr",
                    "mgr": "pip3",
                },
                {
                    "name": "cmgr",
                    "command": "cmgr",
                    "manager": "pip3",
                }
            ]
            self.assertTrue(cmgr.ensure_packages(packages))


if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)

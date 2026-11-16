import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from app import render  # noqa: E402


class RenderTest(unittest.TestCase):
    def test_shows_environment_and_db(self):
        text = render({"APP_ENV": "staging", "DB_HOST": "staging-db", "APP_VERSION": "abc1234"})
        self.assertIn("staging", text)
        self.assertIn("staging-db", text)
        self.assertIn("abc1234", text)

    def test_never_shows_password_value(self):
        text = render({"DB_PASSWORD": "super-secret"})
        self.assertIn("設定あり", text)
        self.assertNotIn("super-secret", text)

    def test_defaults_to_local(self):
        text = render({})
        self.assertIn("local", text)
        self.assertIn("設定なし", text)


if __name__ == "__main__":
    unittest.main()

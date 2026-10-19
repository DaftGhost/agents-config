import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "ratecli", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


class ConvertCommandTests(unittest.TestCase):
    def test_convert_prints_text(self):
        result = run_cli("convert", "100", "USD", "EUR")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "100.00 USD = 92.00 EUR")
        self.assertEqual(result.stderr, "")

    def test_unsupported_pair_is_an_error(self):
        result = run_cli("convert", "1", "USD", "GBP")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unsupported currency pair", result.stderr)

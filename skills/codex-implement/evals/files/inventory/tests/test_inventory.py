import subprocess
import sys
import unittest
from pathlib import Path

from inventory.models import Item
from inventory.service import Inventory

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args):
    return subprocess.run(
        [sys.executable, "-m", "inventory", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


class InventoryServiceTests(unittest.TestCase):
    def test_find_returns_matching_item(self):
        inventory = Inventory([Item("A-1", "Widget", 2), Item("A-2", "Gadget", 5)])
        self.assertEqual(inventory.find("A-2").name, "Gadget")

    def test_find_returns_none_for_unknown_sku(self):
        self.assertIsNone(Inventory().find("missing"))


class ListCommandTests(unittest.TestCase):
    def test_list_prints_all_items(self):
        result = run_cli("list")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout.splitlines(),
            [
                "A-1  Widget  2",
                "A-2  Gadget  5",
                "A-3  Gizmo  0",
                "A-4  Doohickey  3",
            ],
        )

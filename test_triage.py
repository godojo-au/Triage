import tempfile
import unittest
from pathlib import Path

from triage import build_queue, classify


class TriageTests(unittest.TestCase):
    def test_route_and_priority(self):
        result = classify("Login blocked", "Cannot work today")
        self.assertEqual((result["route"], result["priority"]), ("access", "high"))

    def test_duplicate_ids_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "items.csv"
            path.write_text("id,title,description\n1,First,Text\n1,Second,Text\n")
            with self.assertRaisesRegex(ValueError, "unique"):
                build_queue(path)

    def test_review_required(self):
        queue = build_queue(Path(__file__).parent / "examples/items.csv")
        self.assertEqual(len(queue), 4)
        self.assertTrue(all(item["status"] == "needs_review" for item in queue))
        self.assertEqual(queue[0]["description"], "New starter cannot access the dashboard")


if __name__ == "__main__":
    unittest.main()

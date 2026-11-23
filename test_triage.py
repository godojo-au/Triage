import tempfile
import unittest
import io
import json
from pathlib import Path
from unittest.mock import patch

from triage import ai_suggestion, build_queue, classify, retrieve_examples


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

    def test_retrieval_uses_relevant_example(self):
        examples = retrieve_examples("Invoice mismatch", "Please review amount")
        self.assertEqual(examples[0]["id"], "K-02")

    def test_local_model_response_is_validated(self):
        response = {"message": {"content": json.dumps({"route": "billing", "priority": "normal", "reason": "Invoice question"})}}
        with patch("triage.urllib.request.urlopen", return_value=io.BytesIO(json.dumps(response).encode())):
            result = ai_suggestion("Invoice", "Question", "ollama", "local-model", [])
        self.assertEqual(result["route"], "billing")


if __name__ == "__main__":
    unittest.main()

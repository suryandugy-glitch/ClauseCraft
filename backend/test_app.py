import unittest
from unittest.mock import patch

import fitz
from fastapi.testclient import TestClient

from app.main import app


class ContractFlowTest(unittest.TestCase):
    def setUp(self):
        provider = patch("app.main.ai_enabled", return_value=False)
        provider.start()
        self.addCleanup(provider.stop)
        self.client = TestClient(app)
        with fitz.open() as document:
            page = document.new_page()
            page.insert_text((50, 50), "1. The tenant must pay rent.\n"
                                       "2. The tenant shall not sublet.\n"
                                       "3. The contract automatically renews. <script>demo</script>")
            self.pdf = document.tobytes()

    def upload(self, endpoint, content=None):
        return self.client.post(endpoint, files={
            "file": ("sample.pdf", self.pdf if content is None else content, "application/pdf")
        })

    def test_pdf_analysis_and_report(self):
        response = self.upload("/api/process")
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(len(result["original_clauses"]), 3)
        self.assertEqual(result["triples_per_clause"][1][0]["modality"], "prohibition")
        self.assertGreater(result["risk_scores"][2], 0.7)
        self.assertFalse(result["ai_enabled"])
        report = self.upload("/api/export")
        self.assertEqual(report.status_code, 200)
        self.assertIn("attachment", report.headers["content-disposition"])
        self.assertIn("&lt;script&gt;", report.text)
        self.assertNotIn("<script>", report.text)

    def test_invalid_pdf_can_be_rejected(self):
        self.assertEqual(self.upload("/api/process", b"invalid").status_code, 400)
        self.assertEqual(self.client.get("/health").json(), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()

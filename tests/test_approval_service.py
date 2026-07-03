"""
영업일지 결재 서비스 모듈에 대한 단위 테스트.
"""
import unittest
import json
from approval_service import (
    submit_report,
    approve_report,
    reject_report,
    withdraw_report,
)
from sales_report_service import create_report
from customer_service import create_customer

CUSTOMERS_FILE = "data/customers.json"
REPORTS_FILE = "data/sales_reports.json"


class TestApprovalService(unittest.TestCase):
    """영업일지 결재 상태 전이 기능 테스트"""

    def setUp(self):
        """각 테스트 전에 빈 데이터로 초기화"""
        with open(CUSTOMERS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        with open(REPORTS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    def _insert_draft_report(self) -> str:
        """DRAFT 상태의 샘플 영업일지를 등록하고 report_id를 반환한다."""
        success, result = create_customer("테스트 회사", "김철수", "kim@test.com")
        self.assertTrue(success)
        cid = result["customer_id"]
        success, result = create_report(cid, "2026-07-03", "방문 상담 진행")
        self.assertTrue(success)
        return result["report_id"]

    def _set_status(self, report_id: str, status: str):
        """영업일지 상태를 직접 변경한다. (테스트 헬퍼)"""
        with open(REPORTS_FILE, "r", encoding="utf-8") as f:
            reports = json.load(f)
        for r in reports:
            if r["report_id"] == report_id:
                r["status"] = status
                break
        with open(REPORTS_FILE, "w", encoding="utf-8") as f:
            json.dump(reports, f, ensure_ascii=False, indent=2)

    # --- submit (DRAFT → SUBMITTED) ---

    def test_submit_draft_success(self):
        """DRAFT 상태에서 submit 성공"""
        rid = self._insert_draft_report()
        success, result = submit_report(rid)
        self.assertTrue(success)
        self.assertEqual(result["status"], "SUBMITTED")

    def test_submit_already_submitted(self):
        """SUBMITTED 상태에서 submit 차단"""
        rid = self._insert_draft_report()
        submit_report(rid)  # DRAFT → SUBMITTED
        success, msg = submit_report(rid)
        self.assertFalse(success)
        self.assertIn("SUBMITTED 상태에서 submit할 수 없습니다", msg)

    def test_submit_approved(self):
        """APPROVED 상태에서 submit 차단"""
        rid = self._insert_draft_report()
        submit_report(rid)
        approve_report(rid)  # SUBMITTED → APPROVED
        success, msg = submit_report(rid)
        self.assertFalse(success)
        self.assertIn("APPROVED 상태에서 submit할 수 없습니다", msg)

    def test_submit_rejected(self):
        """REJECTED 상태에서 submit 차단"""
        rid = self._insert_draft_report()
        submit_report(rid)
        reject_report(rid)  # SUBMITTED → REJECTED
        success, msg = submit_report(rid)
        self.assertFalse(success)
        self.assertIn("REJECTED 상태에서 submit할 수 없습니다", msg)

    def test_submit_not_found(self):
        """존재하지 않는 ID로 submit 실패"""
        success, msg = submit_report("R999")
        self.assertFalse(success)
        self.assertIn("찾을 수 없습니다", msg)

    # --- approve (SUBMITTED → APPROVED) ---

    def test_approve_submitted_success(self):
        """SUBMITTED 상태에서 approve 성공"""
        rid = self._insert_draft_report()
        submit_report(rid)
        success, result = approve_report(rid)
        self.assertTrue(success)
        self.assertEqual(result["status"], "APPROVED")

    def test_approve_draft(self):
        """DRAFT 상태에서 approve 차단"""
        rid = self._insert_draft_report()
        success, msg = approve_report(rid)
        self.assertFalse(success)
        self.assertIn("DRAFT 상태에서 approve할 수 없습니다", msg)

    def test_approve_approved(self):
        """APPROVED 상태에서 approve 차단"""
        rid = self._insert_draft_report()
        submit_report(rid)
        approve_report(rid)
        success, msg = approve_report(rid)
        self.assertFalse(success)
        self.assertIn("APPROVED 상태에서 approve할 수 없습니다", msg)

    def test_approve_not_found(self):
        """존재하지 않는 ID로 approve 실패"""
        success, msg = approve_report("R999")
        self.assertFalse(success)
        self.assertIn("찾을 수 없습니다", msg)

    # --- reject (SUBMITTED → REJECTED) ---

    def test_reject_submitted_success(self):
        """SUBMITTED 상태에서 reject 성공"""
        rid = self._insert_draft_report()
        submit_report(rid)
        success, result = reject_report(rid)
        self.assertTrue(success)
        self.assertEqual(result["status"], "REJECTED")

    def test_reject_draft(self):
        """DRAFT 상태에서 reject 차단"""
        rid = self._insert_draft_report()
        success, msg = reject_report(rid)
        self.assertFalse(success)
        self.assertIn("DRAFT 상태에서 reject할 수 없습니다", msg)

    def test_reject_approved(self):
        """APPROVED 상태에서 reject 차단"""
        rid = self._insert_draft_report()
        submit_report(rid)
        approve_report(rid)
        success, msg = reject_report(rid)
        self.assertFalse(success)
        self.assertIn("APPROVED 상태에서 reject할 수 없습니다", msg)

    # --- withdraw (SUBMITTED → DRAFT) ---

    def test_withdraw_submitted_success(self):
        """SUBMITTED 상태에서 withdraw 성공"""
        rid = self._insert_draft_report()
        submit_report(rid)
        success, result = withdraw_report(rid)
        self.assertTrue(success)
        self.assertEqual(result["status"], "DRAFT")

    def test_withdraw_draft(self):
        """DRAFT 상태에서 withdraw 차단"""
        rid = self._insert_draft_report()
        success, msg = withdraw_report(rid)
        self.assertFalse(success)
        self.assertIn("DRAFT 상태에서 withdraw할 수 없습니다", msg)

    def test_withdraw_approved(self):
        """APPROVED 상태에서 withdraw 차단"""
        rid = self._insert_draft_report()
        submit_report(rid)
        approve_report(rid)
        success, msg = withdraw_report(rid)
        self.assertFalse(success)
        self.assertIn("APPROVED 상태에서 withdraw할 수 없습니다", msg)

    def tearDown(self):
        """각 테스트 후에 빈 데이터로 초기화"""
        with open(CUSTOMERS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        with open(REPORTS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    unittest.main()
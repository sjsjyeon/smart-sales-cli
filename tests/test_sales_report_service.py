"""
영업일지 서비스 모듈에 대한 단위 테스트.
"""
import unittest
import json
from sales_report_service import (
    create_report,
    get_all_reports,
    get_report_by_id,
    update_report,
    _generate_report_id,
)
from customer_service import create_customer

CUSTOMERS_FILE = "data/customers.json"
REPORTS_FILE = "data/sales_reports.json"


class TestSalesReportService(unittest.TestCase):
    """영업일지 서비스 CRUD 기능 테스트"""

    def setUp(self):
        """각 테스트 전에 빈 데이터로 초기화"""
        with open(CUSTOMERS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        with open(REPORTS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    def _insert_sample_customer(self) -> str:
        """샘플 고객사를 등록하고 customer_id를 반환한다."""
        success, result = create_customer("테스트 회사", "김철수", "kim@test.com")
        self.assertTrue(success)
        return result["customer_id"]

    def _insert_sample_report(self, customer_id: str) -> str:
        """샘플 영업일지를 등록하고 report_id를 반환한다."""
        success, result = create_report(customer_id, "2026-07-03", "방문 상담 진행")
        self.assertTrue(success)
        return result["report_id"]

    # --- _generate_report_id 테스트 ---

    def test_generate_id_empty(self):
        """빈 리스트에서 ID는 R001"""
        rid = _generate_report_id([])
        self.assertEqual(rid, "R001")

    def test_generate_id_incremental(self):
        """기존 ID가 R002면 새 ID는 R003"""
        reports = [{"report_id": "R001"}, {"report_id": "R002"}]
        rid = _generate_report_id(reports)
        self.assertEqual(rid, "R003")

    def test_generate_id_non_standard(self):
        """ID 형식이 다른 영업일지가 있어도 정상 동작"""
        reports = [{"report_id": "X001"}, {"report_id": "R001"}]
        rid = _generate_report_id(reports)
        self.assertEqual(rid, "R002")

    # --- create_report 테스트 ---

    def test_create_report_success(self):
        """정상적인 입력으로 영업일지 등록 성공"""
        cid = self._insert_sample_customer()
        success, result = create_report(cid, "2026-07-03", "고객 미팅 진행")
        self.assertTrue(success)
        self.assertEqual(result["customer_id"], cid)
        self.assertEqual(result["customer_name"], "테스트 회사")
        self.assertEqual(result["date"], "2026-07-03")
        self.assertEqual(result["content"], "고객 미팅 진행")
        self.assertEqual(result["status"], "DRAFT")
        self.assertTrue(result["report_id"].startswith("R"))

    def test_create_report_empty_customer_id(self):
        """고객사 ID가 빈 문자열이면 등록 실패"""
        success, msg = create_report("", "2026-07-03", "내용")
        self.assertFalse(success)
        self.assertIn("고객사 ID", msg)

    def test_create_report_empty_date(self):
        """영업일이 빈 문자열이면 등록 실패"""
        cid = self._insert_sample_customer()
        success, msg = create_report(cid, "", "내용")
        self.assertFalse(success)
        self.assertIn("영업일", msg)

    def test_create_report_empty_content(self):
        """영업일지 내용이 빈 문자열이면 등록 실패"""
        cid = self._insert_sample_customer()
        success, msg = create_report(cid, "2026-07-03", "")
        self.assertFalse(success)
        self.assertIn("영업일지 내용", msg)

    def test_create_report_invalid_date_format(self):
        """날짜 형식이 잘못되면 등록 실패"""
        cid = self._insert_sample_customer()
        success, msg = create_report(cid, "2026/07/03", "내용")
        self.assertFalse(success)
        self.assertIn("날짜", msg)

    def test_create_report_non_existent_customer(self):
        """존재하지 않는 고객사 ID로 등록 시 실패"""
        success, msg = create_report("C999", "2026-07-03", "내용")
        self.assertFalse(success)
        self.assertIn("찾을 수 없습니다", msg)

    def test_create_report_auto_increment_id(self):
        """순차적으로 등록 시 ID가 자동 증가하는지 확인"""
        cid = self._insert_sample_customer()
        rid1 = self._insert_sample_report(cid)
        self.assertEqual(rid1, "R001")
        success, result = create_report(cid, "2026-07-04", "두 번째 영업일지")
        self.assertTrue(success)
        self.assertEqual(result["report_id"], "R002")

    # --- get_all_reports 테스트 ---

    def test_get_all_reports_empty(self):
        """데이터가 없으면 빈 리스트 반환"""
        result = get_all_reports()
        self.assertEqual(result, [])

    def test_get_all_reports_with_data(self):
        """등록된 영업일지 전체 목록 반환"""
        cid = self._insert_sample_customer()
        self._insert_sample_report(cid)
        self._insert_sample_report(cid)
        result = get_all_reports()
        self.assertEqual(len(result), 2)

    # --- get_report_by_id 테스트 ---

    def test_get_report_by_id_found(self):
        """존재하는 ID로 조회 성공"""
        cid = self._insert_sample_customer()
        rid = self._insert_sample_report(cid)
        r = get_report_by_id(rid)
        self.assertIsNotNone(r)
        self.assertEqual(r["report_id"], rid)

    def test_get_report_by_id_not_found(self):
        """존재하지 않는 ID 조회 시 None 반환"""
        r = get_report_by_id("R999")
        self.assertIsNone(r)

    # --- update_report 테스트 ---

    def test_update_report_success(self):
        """정상적인 입력으로 영업일지 수정 성공"""
        cid = self._insert_sample_customer()
        rid = self._insert_sample_report(cid)
        success, result = update_report(rid, "2026-07-10", "수정된 내용")
        self.assertTrue(success)
        self.assertEqual(result["date"], "2026-07-10")
        self.assertEqual(result["content"], "수정된 내용")
        # customer_id와 customer_name은 변경되지 않음
        self.assertEqual(result["customer_id"], cid)
        self.assertEqual(result["customer_name"], "테스트 회사")

    def test_update_report_not_found(self):
        """존재하지 않는 ID 수정 시 실패"""
        success, msg = update_report("R999", "2026-07-10", "내용")
        self.assertFalse(success)
        self.assertIn("찾을 수 없습니다", msg)

    def test_update_report_approved_status(self):
        """APPROVED 상태의 영업일지는 수정 실패"""
        cid = self._insert_sample_customer()
        rid = self._insert_sample_report(cid)
        # 상태를 APPROVED로 변경
        reports = get_all_reports()
        for r in reports:
            if r["report_id"] == rid:
                r["status"] = "APPROVED"
                break
        with open(REPORTS_FILE, "w", encoding="utf-8") as f:
            json.dump(reports, f, ensure_ascii=False, indent=2)

        success, msg = update_report(rid, "2026-07-10", "수정 시도")
        self.assertFalse(success)
        self.assertIn("승인된 영업일지", msg)

    def tearDown(self):
        """각 테스트 후에 빈 데이터로 초기화"""
        with open(CUSTOMERS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
        with open(REPORTS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    unittest.main()
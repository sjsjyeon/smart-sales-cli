"""
고객사 서비스 모듈에 대한 단위 테스트.
"""
import unittest
import os
import json
from customer_service import (
    create_customer,
    get_all_customers,
    get_customer_by_id,
    search_customers,
    update_customer,
    delete_customer,
    _generate_customer_id,
)

CUSTOMERS_FILE = "data/customers.json"


class TestCustomerService(unittest.TestCase):
    """고객사 서비스 CRUD 기능 테스트"""

    def setUp(self):
        """각 테스트 전에 빈 데이터로 초기화"""
        with open(CUSTOMERS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    def _insert_sample_data(self):
        """샘플 고객사 2개를 데이터 파일에 미리 등록한다."""
        sample = [
            {
                "customer_id": "C001",
                "customer_name": "테스트 회사",
                "manager_name": "김철수",
                "email": "kim@test.com",
            },
            {
                "customer_id": "C002",
                "customer_name": "샘플 주식회사",
                "manager_name": "이영희",
                "email": "lee@sample.com",
            },
        ]
        with open(CUSTOMERS_FILE, "w", encoding="utf-8") as f:
            json.dump(sample, f, ensure_ascii=False, indent=2)

    # --- _generate_customer_id 테스트 ---

    def test_generate_id_empty(self):
        """빈 리스트에서 ID는 C001"""
        cid = _generate_customer_id([])
        self.assertEqual(cid, "C001")

    def test_generate_id_incremental(self):
        """기존 ID가 C002면 새 ID는 C003"""
        customers = [{"customer_id": "C001"}, {"customer_id": "C002"}]
        cid = _generate_customer_id(customers)
        self.assertEqual(cid, "C003")

    def test_generate_id_non_standard(self):
        """ID 형식이 다른 고객사가 있어도 정상 동작"""
        customers = [{"customer_id": "X001"}, {"customer_id": "C001"}]
        cid = _generate_customer_id(customers)
        self.assertEqual(cid, "C002")

    # --- create_customer 테스트 ---

    def test_create_customer_success(self):
        """정상적인 입력으로 고객사 등록 성공"""
        success, result = create_customer("신규 회사", "박민수", "park@new.com")
        self.assertTrue(success)
        self.assertEqual(result["customer_name"], "신규 회사")
        self.assertEqual(result["manager_name"], "박민수")
        self.assertEqual(result["email"], "park@new.com")
        self.assertTrue(result["customer_id"].startswith("C"))

    def test_create_customer_empty_name(self):
        """고객사명이 빈 문자열이면 등록 실패"""
        success, msg = create_customer("", "담당자", "email@test.com")
        self.assertFalse(success)
        self.assertIn("고객사명", msg)

    def test_create_customer_blank_name(self):
        """고객사명이 공백만 있으면 등록 실패"""
        success, msg = create_customer("   ", "담당자", "email@test.com")
        self.assertFalse(success)
        self.assertIn("고객사명", msg)

    def test_create_customer_empty_manager(self):
        """담당자명이 빈 문자열이면 등록 실패"""
        success, msg = create_customer("회사명", "", "email@test.com")
        self.assertFalse(success)
        self.assertIn("담당자명", msg)

    def test_create_customer_empty_email(self):
        """이메일이 빈 문자열이면 등록 실패"""
        success, msg = create_customer("회사명", "담당자", "")
        self.assertFalse(success)
        self.assertIn("이메일", msg)

    def test_create_customer_invalid_email(self):
        """이메일 형식이 잘못되면 등록 실패"""
        success, msg = create_customer("회사명", "담당자", "invalid-email")
        self.assertFalse(success)
        self.assertIn("이메일", msg)

    def test_create_customer_duplicate_email(self):
        """중복 이메일로 등록 시도 시 실패"""
        self._insert_sample_data()
        success, msg = create_customer("또 다른 회사", "홍길동", "kim@test.com")
        self.assertFalse(success)
        self.assertIn("이미 등록된 이메일", msg)

    def test_create_customer_auto_increment_id(self):
        """순차적으로 등록 시 ID가 자동 증가하는지 확인"""
        self._insert_sample_data()
        success, result = create_customer("세번째 회사", "최지훈", "choi@third.com")
        self.assertTrue(success)
        self.assertEqual(result["customer_id"], "C003")

    # --- get_all_customers 테스트 ---

    def test_get_all_customers_empty(self):
        """데이터가 없으면 빈 리스트 반환"""
        result = get_all_customers()
        self.assertEqual(result, [])

    def test_get_all_customers_with_data(self):
        """등록된 고객사 전체 목록 반환"""
        self._insert_sample_data()
        result = get_all_customers()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["customer_id"], "C001")
        self.assertEqual(result[1]["customer_id"], "C002")

    # --- get_customer_by_id 테스트 ---

    def test_get_customer_by_id_found(self):
        """존재하는 ID로 조회 성공"""
        self._insert_sample_data()
        c = get_customer_by_id("C001")
        self.assertIsNotNone(c)
        self.assertEqual(c["customer_name"], "테스트 회사")

    def test_get_customer_by_id_not_found(self):
        """존재하지 않는 ID 조회 시 None 반환"""
        self._insert_sample_data()
        c = get_customer_by_id("C999")
        self.assertIsNone(c)

    def test_get_customer_by_id_empty_string(self):
        """빈 문자열로 조회 시 None 반환"""
        c = get_customer_by_id("")
        self.assertIsNone(c)

    # --- update_customer 테스트 ---

    def test_update_customer_success(self):
        """정상적인 입력으로 고객사 정보 수정 성공"""
        self._insert_sample_data()
        success, result = update_customer("C001", "변경된 회사", "김철수", "kim_new@test.com")
        self.assertTrue(success)
        self.assertEqual(result["customer_name"], "변경된 회사")
        self.assertEqual(result["email"], "kim_new@test.com")

    def test_update_customer_not_found(self):
        """존재하지 않는 ID 수정 시 실패"""
        success, msg = update_customer("C999", "이름", "담당자", "email@test.com")
        self.assertFalse(success)
        self.assertIn("찾을 수 없습니다", msg)

    def test_update_customer_duplicate_email(self):
        """다른 고객사가 사용 중인 이메일로 수정 시 실패"""
        self._insert_sample_data()
        success, msg = update_customer("C001", "테스트 회사", "김철수", "lee@sample.com")
        self.assertFalse(success)
        self.assertIn("이미 사용 중인 이메일", msg)

    # --- delete_customer 테스트 ---

    def test_delete_customer_success(self):
        """존재하는 고객사 삭제 성공"""
        self._insert_sample_data()
        success, msg = delete_customer("C001")
        self.assertTrue(success)
        self.assertIn("삭제", msg)
        # 실제로 삭제되었는지 확인
        remaining = get_all_customers()
        self.assertEqual(len(remaining), 1)
        self.assertEqual(remaining[0]["customer_id"], "C002")

    def test_delete_customer_not_found(self):
        """존재하지 않는 ID 삭제 시 실패"""
        success, msg = delete_customer("C999")
        self.assertFalse(success)
        self.assertIn("찾을 수 없습니다", msg)

    # --- search_customers 테스트 ---

    def test_search_by_customer_name(self):
        """고객사명으로 검색"""
        self._insert_sample_data()
        results = search_customers("테스트")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["customer_id"], "C001")

    def test_search_by_manager_name(self):
        """담당자명으로 검색"""
        self._insert_sample_data()
        results = search_customers("이영희")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["customer_id"], "C002")

    def test_search_by_email(self):
        """이메일로 검색"""
        self._insert_sample_data()
        results = search_customers("kim@test.com")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["customer_id"], "C001")

    def test_search_case_insensitive(self):
        """대소문자 구분 없이 검색"""
        self._insert_sample_data()
        results = search_customers("KIM@TEST.COM")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["customer_id"], "C001")

    def test_search_empty_keyword(self):
        """빈 문자열 검색어는 빈 리스트 반환"""
        self._insert_sample_data()
        results = search_customers("")
        self.assertEqual(results, [])

    def test_search_blank_keyword(self):
        """공백만 있는 검색어는 빈 리스트 반환"""
        self._insert_sample_data()
        results = search_customers("   ")
        self.assertEqual(results, [])

    def test_search_no_match(self):
        """존재하지 않는 검색어는 빈 리스트 반환"""
        self._insert_sample_data()
        results = search_customers("존재하지않음")
        self.assertEqual(results, [])

    def test_search_partial_match(self):
        """부분 일치 검색"""
        self._insert_sample_data()
        results = search_customers("회사")
        self.assertEqual(len(results), 2)

    def tearDown(self):
        """각 테스트 후에 빈 데이터로 초기화"""
        with open(CUSTOMERS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    unittest.main()
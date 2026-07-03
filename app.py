"""
Smart Sales CLI - 메인 진입점
"""
import sys
import customer_service


def show_menu():
    """메인 메뉴를 화면에 출력한다."""
    print("\n" + "=" * 40)
    print("          Smart Sales CLI")
    print("=" * 40)
    print("  1. 고객사 관리")
    print("  2. 영업일지 관리")
    print("  3. 영업일지 결재")
    print("  4. 고객사별 활동 요약")
    print("  5. CSV 내보내기")
    print("  0. 종료")
    print("=" * 40)


def show_customer_menu():
    """고객사 관리 하위 메뉴를 화면에 출력한다."""
    print("\n" + "-" * 40)
    print("        고객사 관리")
    print("-" * 40)
    print("  1. 고객사 등록")
    print("  2. 고객사 목록")
    print("  3. 고객사 상세 조회")
    print("  4. 고객사 수정")
    print("  5. 고객사 삭제")
    print("  6. 고객사 검색")
    print("  0. 뒤로 가기")
    print("-" * 40)


def handle_customer_menu():
    """고객사 관리 하위 메뉴를 처리한다."""
    while True:
        show_customer_menu()
        choice = input("메뉴를 선택하세요: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            handle_create_customer()
        elif choice == "2":
            handle_list_customers()
        elif choice == "3":
            handle_get_customer()
        elif choice == "4":
            handle_update_customer()
        elif choice == "5":
            handle_delete_customer()
        elif choice == "6":
            handle_search_customers()
        else:
            print("잘못된 입력입니다. 0~6 사이의 숫자를 입력하세요.")


def handle_create_customer():
    """고객사 등록을 처리한다."""
    print("\n--- 고객사 등록 ---")
    name = input("고객사명: ").strip()
    manager = input("담당자명: ").strip()
    email = input("이메일: ").strip()

    success, result = customer_service.create_customer(name, manager, email)
    if success:
        c = result
        print(f"등록 완료: {c['customer_id']} - {c['customer_name']}")
    else:
        print(f"오류: {result}")


def handle_list_customers():
    """고객사 목록을 출력한다."""
    customers = customer_service.get_all_customers()
    if not customers:
        print("\n등록된 고객사가 없습니다.")
        return
    print("\n--- 고객사 목록 ---")
    print(f"{'ID':<6} {'고객사명':<20} {'담당자':<10} {'이메일':<25}")
    print("-" * 61)
    for c in customers:
        print(f"{c['customer_id']:<6} {c['customer_name']:<20} {c['manager_name']:<10} {c['email']:<25}")


def handle_get_customer():
    """고객사 상세 조회를 처리한다."""
    print("\n--- 고객사 상세 조회 ---")
    cid = input("고객사 ID: ").strip()
    c = customer_service.get_customer_by_id(cid)
    if c:
        print(f"고객사 ID: {c['customer_id']}")
        print(f"고객사명: {c['customer_name']}")
        print(f"담당자명: {c['manager_name']}")
        print(f"이메일: {c['email']}")
    else:
        print(f"고객사 ID '{cid}'를 찾을 수 없습니다.")


def handle_update_customer():
    """고객사 수정을 처리한다."""
    print("\n--- 고객사 수정 ---")
    cid = input("고객사 ID: ").strip()
    name = input("새 고객사명: ").strip()
    manager = input("새 담당자명: ").strip()
    email = input("새 이메일: ").strip()

    success, result = customer_service.update_customer(cid, name, manager, email)
    if success:
        c = result
        print(f"수정 완료: {c['customer_id']} - {c['customer_name']}")
    else:
        print(f"오류: {result}")


def handle_search_customers():
    """고객사 검색을 처리한다."""
    print("\n--- 고객사 검색 ---")
    keyword = input("검색어: ").strip()
    results = customer_service.search_customers(keyword)
    if not results:
        print("검색 결과가 없습니다.")
        return
    print(f"\n--- 검색 결과 ({len(results)}건) ---")
    print(f"{'ID':<6} {'고객사명':<20} {'담당자':<10} {'이메일':<25}")
    print("-" * 61)
    for c in results:
        print(f"{c['customer_id']:<6} {c['customer_name']:<20} {c['manager_name']:<10} {c['email']:<25}")


def handle_delete_customer():
    """고객사 삭제를 처리한다."""
    print("\n--- 고객사 삭제 ---")
    cid = input("고객사 ID: ").strip()
    success, result = customer_service.delete_customer(cid)
    if success:
        print(result)
    else:
        print(f"오류: {result}")


def main():
    """CLI 메인 루프"""
    while True:
        show_menu()
        choice = input("메뉴를 선택하세요: ").strip()

        if choice == "0":
            print("프로그램을 종료합니다.")
            sys.exit(0)
        elif choice == "1":
            handle_customer_menu()
        elif choice == "2":
            print("[미구현] 영업일지 관리")
        elif choice == "3":
            print("[미구현] 영업일지 결재")
        elif choice == "4":
            print("[미구현] 고객사별 활동 요약")
        elif choice == "5":
            print("[미구현] CSV 내보내기")
        else:
            print("잘못된 입력입니다. 0~5 사이의 숫자를 입력하세요.")


if __name__ == "__main__":
    main()

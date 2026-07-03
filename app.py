"""
Smart Sales CLI - 메인 진입점
"""
import sys


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


def main():
    """CLI 메인 루프"""
    while True:
        show_menu()
        choice = input("메뉴를 선택하세요: ").strip()

        if choice == "0":
            print("프로그램을 종료합니다.")
            sys.exit(0)
        elif choice == "1":
            print("[미구현] 고객사 관리")
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
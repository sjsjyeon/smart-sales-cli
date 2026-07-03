"""
고객사 등록, 목록, 상세 조회, 수정, 삭제를 담당하는 모듈.
"""
from storage import load_json, save_json
from validators import validate_required, validate_email

CUSTOMERS_FILE = "customers.json"


def _generate_customer_id(customers: list) -> str:
    """고객사 ID를 자동 생성한다. (C001, C002, ...)

    Args:
        customers: 기존 고객사 리스트

    Returns:
        새로운 고객사 ID (예: C003)
    """
    max_num = 0
    for c in customers:
        cid = c.get("customer_id", "")
        if cid.startswith("C") and cid[1:].isdigit():
            num = int(cid[1:])
            if num > max_num:
                max_num = num
    return f"C{max_num + 1:03d}"


def get_all_customers() -> list:
    """전체 고객사 목록을 반환한다."""
    return load_json(CUSTOMERS_FILE)


def search_customers(keyword: str) -> list:
    """검색어로 고객사를 검색한다. (고객사명, 담당자명, 이메일)

    검색은 대소문자를 구분하지 않는다.
    빈 문자열이나 공백만 있는 검색어는 빈 리스트를 반환한다.

    Args:
        keyword: 검색어

    Returns:
        검색 조건에 일치하는 고객사 리스트
    """
    if not keyword or not keyword.strip():
        return []

    keyword_lower = keyword.strip().lower()
    customers = load_json(CUSTOMERS_FILE)
    result = []
    for c in customers:
        if (keyword_lower in c.get("customer_name", "").lower()
                or keyword_lower in c.get("manager_name", "").lower()
                or keyword_lower in c.get("email", "").lower()):
            result.append(c)
    return result


def get_customer_by_id(customer_id: str) -> dict | None:
    """고객사 ID로 단건 조회한다.

    Args:
        customer_id: 조회할 고객사 ID

    Returns:
        고객사 딕셔너리, 존재하지 않으면 None
    """
    customers = load_json(CUSTOMERS_FILE)
    for c in customers:
        if c.get("customer_id") == customer_id:
            return c
    return None


def create_customer(customer_name: str, manager_name: str, email: str) -> tuple:
    """신규 고객사를 등록한다.

    Args:
        customer_name: 고객사명
        manager_name: 담당자명
        email: 이메일 주소

    Returns:
        (성공 여부, 메시지 또는 생성된 고객사 딕셔너리)
    """
    # 입력값 검증
    err = validate_required(customer_name, "고객사명")
    if err:
        return False, err
    err = validate_required(manager_name, "담당자명")
    if err:
        return False, err
    err = validate_required(email, "이메일")
    if err:
        return False, err
    err = validate_email(email)
    if err:
        return False, err

    customers = load_json(CUSTOMERS_FILE)

    # 이메일 중복 검사
    for c in customers:
        if c.get("email") == email:
            return False, f"이미 등록된 이메일입니다: {email}"

    new_id = _generate_customer_id(customers)
    new_customer = {
        "customer_id": new_id,
        "customer_name": customer_name.strip(),
        "manager_name": manager_name.strip(),
        "email": email.strip(),
    }
    customers.append(new_customer)
    save_json(CUSTOMERS_FILE, customers)
    return True, new_customer


def update_customer(customer_id: str, customer_name: str, manager_name: str, email: str) -> tuple:
    """고객사 정보를 수정한다.

    Args:
        customer_id: 수정할 고객사 ID
        customer_name: 새 고객사명
        manager_name: 새 담당자명
        email: 새 이메일

    Returns:
        (성공 여부, 메시지 또는 수정된 고객사 딕셔너리)
    """
    # 입력값 검증
    err = validate_required(customer_name, "고객사명")
    if err:
        return False, err
    err = validate_required(manager_name, "담당자명")
    if err:
        return False, err
    err = validate_required(email, "이메일")
    if err:
        return False, err
    err = validate_email(email)
    if err:
        return False, err

    customers = load_json(CUSTOMERS_FILE)
    for c in customers:
        if c.get("customer_id") == customer_id:
            # 다른 고객사의 이메일 중복 검사
            for other in customers:
                if other.get("customer_id") != customer_id and other.get("email") == email:
                    return False, f"다른 고객사에서 이미 사용 중인 이메일입니다: {email}"
            c["customer_name"] = customer_name.strip()
            c["manager_name"] = manager_name.strip()
            c["email"] = email.strip()
            save_json(CUSTOMERS_FILE, customers)
            return True, c

    return False, f"고객사 ID '{customer_id}'를 찾을 수 없습니다."


def delete_customer(customer_id: str) -> tuple:
    """고객사를 삭제한다.

    Args:
        customer_id: 삭제할 고객사 ID

    Returns:
        (성공 여부, 메시지)
    """
    customers = load_json(CUSTOMERS_FILE)
    for i, c in enumerate(customers):
        if c.get("customer_id") == customer_id:
            deleted = customers.pop(i)
            save_json(CUSTOMERS_FILE, customers)
            return True, f"고객사 '{deleted['customer_name']}'을(를) 삭제했습니다."

    return False, f"고객사 ID '{customer_id}'를 찾을 수 없습니다."
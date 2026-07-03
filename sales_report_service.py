"""
영업일지 등록, 목록, 조회, 수정을 담당하는 모듈.
"""
from storage import load_json, save_json
from validators import validate_required, validate_date
from customer_service import get_customer_by_id

REPORTS_FILE = "sales_reports.json"


def _generate_report_id(reports: list) -> str:
    """영업일지 ID를 자동 생성한다. (R001, R002, ...)

    Args:
        reports: 기존 영업일지 리스트

    Returns:
        새로운 영업일지 ID (예: R003)
    """
    max_num = 0
    for r in reports:
        rid = r.get("report_id", "")
        if rid.startswith("R") and rid[1:].isdigit():
            num = int(rid[1:])
            if num > max_num:
                max_num = num
    return f"R{max_num + 1:03d}"


def get_all_reports() -> list:
    """전체 영업일지 목록을 반환한다."""
    return load_json(REPORTS_FILE)


def get_report_by_id(report_id: str) -> dict | None:
    """영업일지 ID로 단건 조회한다.

    Args:
        report_id: 조회할 영업일지 ID

    Returns:
        영업일지 딕셔너리, 존재하지 않으면 None
    """
    reports = load_json(REPORTS_FILE)
    for r in reports:
        if r.get("report_id") == report_id:
            return r
    return None


def create_report(customer_id: str, date: str, content: str) -> tuple:
    """신규 영업일지를 등록한다.

    등록된 고객사에 대해서만 작성 가능하며,
    신규 영업일지는 DRAFT 상태로 저장된다.

    Args:
        customer_id: 고객사 ID
        date: 영업일 (YYYY-MM-DD)
        content: 영업일지 내용

    Returns:
        (성공 여부, 메시지 또는 생성된 영업일지 딕셔너리)
    """
    # 입력값 검증
    err = validate_required(customer_id, "고객사 ID")
    if err:
        return False, err
    err = validate_required(date, "영업일")
    if err:
        return False, err
    err = validate_required(content, "영업일지 내용")
    if err:
        return False, err
    err = validate_date(date)
    if err:
        return False, err

    # 고객사 존재 확인
    customer = get_customer_by_id(customer_id)
    if customer is None:
        return False, f"고객사 ID '{customer_id}'를 찾을 수 없습니다."

    reports = load_json(REPORTS_FILE)
    new_id = _generate_report_id(reports)
    new_report = {
        "report_id": new_id,
        "customer_id": customer_id,
        "customer_name": customer["customer_name"],
        "date": date.strip(),
        "content": content.strip(),
        "status": "DRAFT",
    }
    reports.append(new_report)
    save_json(REPORTS_FILE, reports)
    return True, new_report


def update_report(report_id: str, date: str, content: str) -> tuple:
    """영업일지를 수정한다.

    상태가 APPROVED인 영업일지는 수정할 수 없다.

    Args:
        report_id: 수정할 영업일지 ID
        date: 새 영업일 (YYYY-MM-DD)
        content: 새 영업일지 내용

    Returns:
        (성공 여부, 메시지 또는 수정된 영업일지 딕셔너리)
    """
    # 입력값 검증
    err = validate_required(date, "영업일")
    if err:
        return False, err
    err = validate_required(content, "영업일지 내용")
    if err:
        return False, err
    err = validate_date(date)
    if err:
        return False, err

    reports = load_json(REPORTS_FILE)
    for r in reports:
        if r.get("report_id") == report_id:
            if r.get("status") == "APPROVED":
                return False, "승인된 영업일지는 수정할 수 없습니다."
            r["date"] = date.strip()
            r["content"] = content.strip()
            save_json(REPORTS_FILE, reports)
            return True, r

    return False, f"영업일지 ID '{report_id}'를 찾을 수 없습니다."
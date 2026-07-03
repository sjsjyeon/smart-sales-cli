"""
입력값 검증 함수를 제공하는 모듈.
"""
import re
from datetime import datetime


def validate_required(value: str, field_name: str) -> str | None:
    """필수 입력값이 비어 있는지 검증한다.

    Args:
        value: 입력값
        field_name: 필드명 (오류 메시지에 사용)

    Returns:
        유효하면 None, 유효하지 않으면 오류 메시지 문자열
    """
    if value is None or value.strip() == "":
        return f"{field_name}은(는) 필수 입력 항목입니다."
    return None


def validate_email(email: str) -> str | None:
    """이메일 주소 형식을 검증한다.

    Args:
        email: 이메일 주소

    Returns:
        유효하면 None, 유효하지 않으면 오류 메시지 문자열
    """
    if email is None or email.strip() == "":
        return None  # 필수 검증은 validate_required에서 처리
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email.strip()):
        return "이메일 형식이 올바르지 않습니다."
    return None


def validate_date(date_str: str) -> str | None:
    """날짜 형식(YYYY-MM-DD)을 검증한다.

    Args:
        date_str: 날짜 문자열

    Returns:
        유효하면 None, 유효하지 않으면 오류 메시지 문자열
    """
    if date_str is None or date_str.strip() == "":
        return None  # 필수 검증은 validate_required에서 처리
    date_str = date_str.strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        return "날짜는 YYYY-MM-DD 형식으로 입력해야 합니다."
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return None
    except ValueError:
        return "존재하지 않는 날짜입니다."


def validate_customer_id(customer_id: str) -> str | None:
    """고객사 ID 형식(C001)을 검증한다.

    Args:
        customer_id: 고객사 ID

    Returns:
        유효하면 None, 유효하지 않으면 오류 메시지 문자열
    """
    if customer_id is None or customer_id.strip() == "":
        return None
    if not re.match(r"^C\d{3}$", customer_id.strip()):
        return "고객사 ID는 C001 형식으로 입력해야 합니다."
    return None

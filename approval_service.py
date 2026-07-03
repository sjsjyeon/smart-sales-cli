"""
영업일지 결재 흐름(상태 전이)을 담당하는 모듈.

상태 전이 규칙:
    DRAFT     → submit   → SUBMITTED
    SUBMITTED → approve  → APPROVED
    SUBMITTED → reject   → REJECTED
    SUBMITTED → withdraw → DRAFT
    그 외 전이는 모두 차단
"""
from storage import load_json, save_json

REPORTS_FILE = "sales_reports.json"

_TRANSITIONS = {
    "DRAFT": {"submit": "SUBMITTED"},
    "SUBMITTED": {
        "approve": "APPROVED",
        "reject": "REJECTED",
        "withdraw": "DRAFT",
    },
}


def _get_report(report_id: str) -> tuple:
    """영업일지를 조회한다.

    Args:
        report_id: 영업일지 ID

    Returns:
        (성공 여부, 영업일지 딕셔너리 또는 오류 메시지)
    """
    reports = load_json(REPORTS_FILE)
    for r in reports:
        if r.get("report_id") == report_id:
            return True, r
    return False, f"영업일지 ID '{report_id}'를 찾을 수 없습니다."


def _change_status(report_id: str, action: str) -> tuple:
    """영업일지 상태를 전이한다.

    Args:
        report_id: 영업일지 ID
        action: 실행할 액션 (submit, approve, reject, withdraw)

    Returns:
        (성공 여부, 메시지 또는 변경된 영업일지 딕셔너리)
    """
    found, report_or_msg = _get_report(report_id)
    if not found:
        return False, report_or_msg

    report = report_or_msg
    current_status = report.get("status", "")

    # 현재 상태에서 해당 액션이 가능한지 확인
    allowed = _TRANSITIONS.get(current_status, {})
    if action not in allowed:
        action_names = {
            "submit": "submit",
            "approve": "approve",
            "reject": "reject",
            "withdraw": "withdraw",
        }
        action_name = action_names.get(action, action)
        return False, f"{current_status} 상태에서 {action_name}할 수 없습니다."

    new_status = allowed[action]
    reports = load_json(REPORTS_FILE)
    for r in reports:
        if r.get("report_id") == report_id:
            r["status"] = new_status
            save_json(REPORTS_FILE, reports)
            return True, r

    return False, f"영업일지 ID '{report_id}'를 찾을 수 없습니다."


def submit_report(report_id: str) -> tuple:
    """영업일지를 결재 요청한다. (DRAFT → SUBMITTED)

    Args:
        report_id: 영업일지 ID

    Returns:
        (성공 여부, 메시지 또는 변경된 영업일지 딕셔너리)
    """
    return _change_status(report_id, "submit")


def approve_report(report_id: str) -> tuple:
    """영업일지를 승인한다. (SUBMITTED → APPROVED)

    Args:
        report_id: 영업일지 ID

    Returns:
        (성공 여부, 메시지 또는 변경된 영업일지 딕셔너리)
    """
    return _change_status(report_id, "approve")


def reject_report(report_id: str) -> tuple:
    """영업일지를 반려한다. (SUBMITTED → REJECTED)

    Args:
        report_id: 영업일지 ID

    Returns:
        (성공 여부, 메시지 또는 변경된 영업일지 딕셔너리)
    """
    return _change_status(report_id, "reject")


def withdraw_report(report_id: str) -> tuple:
    """영업일지 결재 요청을 회수한다. (SUBMITTED → DRAFT)

    Args:
        report_id: 영업일지 ID

    Returns:
        (성공 여부, 메시지 또는 변경된 영업일지 딕셔너리)
    """
    return _change_status(report_id, "withdraw")
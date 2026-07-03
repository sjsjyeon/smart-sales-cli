"""
JSON 파일 읽기/쓰기를 담당하는 모듈.
"""
import json
import os


DATA_DIR = "data"


def _get_path(filename: str) -> str:
    """data 폴더 내 파일의 전체 경로를 반환한다."""
    return os.path.join(DATA_DIR, filename)


def load_json(filename: str) -> list:
    """지정된 JSON 파일을 읽어 Python 리스트로 반환한다.

    Args:
        filename: data/ 디렉토리 내의 JSON 파일명 (예: 'customers.json')

    Returns:
        JSON 배열에 해당하는 list. 파일이 없거나 비어 있으면 빈 리스트를 반환한다.
    """
    path = _get_path(filename)
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_json(filename: str, data: list) -> None:
    """Python 리스트를 JSON 파일로 저장한다.

    Args:
        filename: data/ 디렉토리 내의 JSON 파일명 (예: 'customers.json')
        data: 저장할 리스트 객체
    """
    path = _get_path(filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
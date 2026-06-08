from datetime import datetime

ALLOWED_STATUSES = {
    "success",
    "failed"
}

def validate_status(status: str) -> str:

    status_clean = status.strip().lower()

    if status_clean not in ALLOWED_STATUSES:
        raise ValueError("Invalid status")

    return status_clean


def parse_datetime(value: str) -> datetime:

    try:
        return value
    except ValueError:
        raise ValueError(
            "Datetime must be in format 'YYYYMMDD'"
        )

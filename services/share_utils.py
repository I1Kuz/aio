from datetime import datetime, UTC

def utcnow_without_microsec() -> datetime:
    # make time without microseconds
    return datetime.now(UTC).replace(microsecond=0)



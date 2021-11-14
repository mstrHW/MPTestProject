from datetime import datetime
import iso8601


def is_iso8601_format(timestamp_str):
    try:
        datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    except:
        return False
    return True


def from_iso(timestamp_str):
    if is_iso8601_format(timestamp_str):
        return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    else:
        raise ValueError('Timestamp not in iso8601 format')


def to_str(timestamp_dt):
    return timestamp_dt.strftime('%Y%m%d')


def timestamp_to_iso(timestamp):
    return datetime.fromtimestamp(timestamp).isoformat()


def calc_delta(first_timestamp, second_timestamp):
    prev = iso8601.parse_date(first_timestamp)
    next = iso8601.parse_date(second_timestamp)
    delta = int((next - prev).total_seconds() / 60)
    return delta

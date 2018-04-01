from datetime import datetime

def timestamp_to_datetime(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")

def datetime_in_threshold(challenger_dt, base_dt, threshold):
    return abs(challenger_dt - base_dt).seconds <= threshold

def sort_list_by_timestamp(l, reverse=False):
    l.sort(key = lambda r: r["timestamp"], reverse=reverse)

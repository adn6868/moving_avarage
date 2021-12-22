from datetime import date, datetime

def from_timestamp_to_sql_format(timestamp):
    dt_object = datetime.fromtimestamp(timestamp)
    return dt_object.strftime('%Y-%m-%d %H:%M:%S')
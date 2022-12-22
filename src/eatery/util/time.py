from datetime import date, time, datetime
import pytz

def combined_timestamp(date: date, time: time, tzinfo: pytz.timezone) -> int:
    return int(tzinfo.localize(datetime.combine(date, time)).timestamp())

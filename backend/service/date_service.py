import pytz
import contextlib
from datetime import date, datetime, timedelta
from service.framework_service import settings

MONTH_MAP = {
    1: 1,
    2: 1,
    3: 1,
    4: 2,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    9: 3,
    10: 4,
    11: 4,
    12: 4,
}

QUATER_MAP = {
    1: [1, 2, 3],
    2: [4, 5, 6],
    3: [7, 8, 9],
    4: [10, 1, 12],
}


class DateService:
    @staticmethod
    def now(aware=False) -> datetime:
        result = datetime.now()
        return DateService.make_aware(result) if aware else result

    @staticmethod
    def today(aware=False) -> date:
        result = date.today()
        return DateService.make_aware(result) if aware else result


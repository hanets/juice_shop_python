# https://exercism.org/tracks/python/exercises/swift-scheduling
from datetime import datetime, date, time, timedelta, timezone
import math
from zoneinfo import ZoneInfo
import calendar
import pytest


class SwiftScheduling:
    def __init__(self, meeting_start: datetime = None):
        if meeting_start == None:
            meeting_start = datetime.now()
        self.meeting_start = meeting_start

    def transform_fixed_delivery_date(self, date: str) -> datetime:
        match date:
            case "NOW":
                return self.meeting_start + timedelta(hours=2)
            case "ASAP":
                if self.meeting_start.time() < time(13, 0):
                    return self.__combine(0, 17)
                else:
                    return self.__combine(1, 13)
            case "EOW":
                weekday = self.meeting_start.weekday()
                if weekday <= calendar.WEDNESDAY:
                    days_diff = calendar.FRIDAY - weekday
                    return self.__combine(days_diff, 17)
                else:
                    days_diff = calendar.SUNDAY - weekday
                    return self.__combine(days_diff, 20)

        raise ValueError(f"can't find '{date}' mapping")

    def __combine(self, days_diff: int, time_hour: int) -> datetime:
        return datetime.combine(
            self.meeting_start.date() + timedelta(days=days_diff),
            time(time_hour),
            tzinfo=timezone.utc,
        )

    def transform_variable_deliery_date(self, description: str) -> datetime:
        if description.startswith("Q"):
            quarter = int(description[1:])
            current_quarter = math.ceil(self.meeting_start.month / 3)
            match quarter:
                case 1:
                    month = calendar.APRIL
                case 2:
                    month = calendar.JULY
                case 3:
                    month = calendar.OCTOBER
                case 4:
                    month = calendar.JANUARY

            increase_year = quarter == 4 or current_quarter > quarter
            return self.__first_day_of_month(increase_year, month) - timedelta(days=1)
        elif description.endswith("M"):
            month = int(description[:-1])
            current_month = self.meeting_start.month
            return self.__first_day_of_month(current_month > month, month)
        else:
            raise ValueError(f'Incorrect description "{description}"')

    def __first_day_of_month(self, increas_year: bool, month: int) -> datetime:
        year = self.meeting_start.year
        if increas_year:
            year += 1
        next_day = self.meeting_start.replace(
            year=year, month=month, day=1, hour=8, minute=0, second=0, microsecond=0
        )
        return next_day


def test_transform():
    print(SwiftScheduling().transform_fixed_delivery_date("NOW"))
    print(SwiftScheduling().transform_fixed_delivery_date("ASAP"))
    print(SwiftScheduling().transform_fixed_delivery_date("EOW"))


def test_transform_fixed_delivery_date_now():
    base_time = datetime(2024, 6, 1, 10, 0, tzinfo=timezone.utc)
    swift = SwiftScheduling(base_time)
    result = swift.transform_fixed_delivery_date("NOW")
    expected = base_time + timedelta(hours=2)
    assert result == expected


def test_transform_fixed_delivery_date_asap_before_13():
    base_time = datetime(2024, 6, 1, 12, 0, tzinfo=timezone.utc)
    swift = SwiftScheduling(base_time)
    # Should return same day at 17:00
    expected = datetime.combine(base_time.date(), time(17), tzinfo=timezone.utc)
    result = swift.transform_fixed_delivery_date("ASAP")
    assert result == expected


def test_transform_fixed_delivery_date_asap_after_13():
    base_time = datetime(2024, 6, 1, 14, 0, tzinfo=timezone.utc)
    swift = SwiftScheduling(base_time)
    # Should return next day at 13:00
    next_day = base_time.date() + timedelta(days=1)
    expected = datetime.combine(next_day, time(13), tzinfo=timezone.utc)
    result = swift.transform_fixed_delivery_date("ASAP")
    assert result == expected


def test_transform_fixed_delivery_date_eow_before_wednesday():
    # Monday
    base_time = datetime(2024, 6, 3, 10, 0, tzinfo=timezone.utc)
    swift = SwiftScheduling(base_time)
    # Friday is 4 days after Monday (weekday 0)
    expected = datetime.combine(
        base_time.date() + timedelta(days=4), time(17), tzinfo=timezone.utc
    )
    result = swift.transform_fixed_delivery_date("EOW")
    assert result == expected


def test_transform_fixed_delivery_date_eow_after_wednesday():
    # Thursday
    base_time = datetime(2024, 6, 6, 10, 0, tzinfo=timezone.utc)
    swift = SwiftScheduling(base_time)
    # Sunday is 3 days after Thursday (weekday 3)
    expected = datetime.combine(
        base_time.date() + timedelta(days=3), time(20), tzinfo=timezone.utc
    )
    result = swift.transform_fixed_delivery_date("EOW")
    assert result == expected


def test_transform_fixed_delivery_date_invalid():
    swift = SwiftScheduling(datetime(2024, 6, 1, 10, 0, tzinfo=timezone.utc))
    with pytest.raises(ValueError, match="can't find 'INVALID' mapping"):
        swift.transform_fixed_delivery_date("INVALID")


def test_transform_variable_delivery_date_q1_before_april():
    base_time = datetime(2024, 2, 15, 10, 0, tzinfo=timezone.utc)
    swift = SwiftScheduling(base_time)
    # Q1 should return March 31, 2024 at 08:00
    expected = datetime(2024, 3, 31, 8, 0, tzinfo=timezone.utc)
    result = swift.transform_variable_deliery_date("Q1")
    assert result == expected


def test_transform_variable_delivery_date_q2_before_july():
    base_time = datetime(2024, 5, 10, 10, 0, tzinfo=timezone.utc)
    swift = SwiftScheduling(base_time)
    # Q2 should return June 30, 2024 at 08:00
    expected = datetime(2024, 6, 30, 8, 0, tzinfo=timezone.utc)
    result = swift.transform_variable_deliery_date("Q2")
    assert result == expected


def test_transform_variable_delivery_date_q3_before_october():
    base_time = datetime(2024, 8, 20, 10, 0, tzinfo=timezone.utc)
    swift = SwiftScheduling(base_time)
    # Q3 should return September 30, 2024 at 08:00
    expected = datetime(2024, 9, 30, 8, 0, tzinfo=timezone.utc)
    result = swift.transform_variable_deliery_date("Q3")
    assert result == expected


def test_transform_variable_delivery_date_q4_before_january():
    base_time = datetime(2024, 11, 5, 10, 0, tzinfo=timezone.utc)
    swift = SwiftScheduling(base_time)
    # Q4 should return December 31, 2024 at 08:00
    expected = datetime(2024, 12, 31, 8, 0, tzinfo=timezone.utc)
    result = swift.transform_variable_deliery_date("Q4")
    assert result == expected


def test_transform_variable_delivery_date_q1_next_year():
    base_time = datetime(2024, 5, 10, 10, 0, tzinfo=timezone.utc)
    swift = SwiftScheduling(base_time)
    # If current_quarter > quarter + 1, should roll over to next year
    # Here, current_quarter = 2, quarter = 1, so not next year
    expected = datetime(2025, 3, 31, 8, 0, tzinfo=timezone.utc)
    result = swift.transform_variable_deliery_date("Q1")
    assert result == expected


def test_transform_variable_delivery_date_q1_far_future():
    base_time = datetime(2024, 12, 15, 10, 0, tzinfo=timezone.utc)
    swift = SwiftScheduling(base_time)
    # current_quarter = 4, quarter = 2, current_quarter > quarter + 1, so next year
    expected = datetime(2025, 6, 30, 8, 0, tzinfo=timezone.utc)
    result = swift.transform_variable_deliery_date("Q2")
    assert result == expected


def test_transform_variable_delivery_date_invalid_format():
    base_time = datetime(2024, 6, 1, 10, 0, tzinfo=timezone.utc)
    swift = SwiftScheduling(base_time)
    # Should return error
    with pytest.raises(ValueError, match='Incorrect description "SOMETHING"'):
        swift.transform_variable_deliery_date("SOMETHING")

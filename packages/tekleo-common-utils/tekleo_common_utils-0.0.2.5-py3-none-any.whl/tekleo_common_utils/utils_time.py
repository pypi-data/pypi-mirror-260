from datetime import datetime, tzinfo
from typing import List

import pytz
import tzlocal
import calendar
from injectable import injectable

DEFAULT_TZ = pytz.utc
DEFAULT_DATE_FORMAT = '%d.%m.%Y %H:%M:%S (%z)'


@injectable
class UtilsTime:
    # Timezones
    #-------------------------------------------------------------------------------------------------------------------
    def get_timezone(self, name: str) -> tzinfo:
        return pytz.timezone(name)

    def get_timezone_local(self) -> tzinfo:
        return tzlocal.get_localzone()

    def get_timezone_utc(self) -> tzinfo:
        return self.get_timezone("UTC")

    def get_timezone_pst(self) -> tzinfo:
        return self.get_timezone("US/Pacific")
    #-------------------------------------------------------------------------------------------------------------------



    # Timestamps
    #-------------------------------------------------------------------------------------------------------------------
    def get_timestamp_ms_now(self, timezone: tzinfo = DEFAULT_TZ) -> int:
        date_time_object = datetime.now(tz=timezone)
        timestamp_s = date_time_object.timestamp()
        return int(round(timestamp_s * 1000))

    def get_timestamp_ms(self, year: int, month: int, day: int, hour: int, minute: int, second: int, timezone: tzinfo = DEFAULT_TZ) -> int:
        date_time_object = datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second, tzinfo=timezone).astimezone(timezone)
        timestamp_s = date_time_object.timestamp()
        return int(round(timestamp_s * 1000))

    def get_timestamp_ms_day(self, year: int, month: int, day: int, timezone: tzinfo = DEFAULT_TZ) -> int:
        return self.get_timestamp_ms(year, month, day, hour=12, minute=0, second=0, timezone=timezone)
    #-------------------------------------------------------------------------------------------------------------------



    # Formating to string / parsing from string
    #-------------------------------------------------------------------------------------------------------------------
    def format_timestamp_ms(self, timestamp_ms: int, timezone: tzinfo = DEFAULT_TZ, date_format: str = DEFAULT_DATE_FORMAT) -> str:
        date_time_object = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone)
        return date_time_object.strftime(date_format)

    def parse_timestamp_ms(self, date_str: str, date_format: str = DEFAULT_DATE_FORMAT) -> int:
        date_time_object = datetime.strptime(date_str, date_format)
        timestamp_s = date_time_object.timestamp()
        return int(round(timestamp_s * 1000))

    # This was used specifically in Ortho2 dates
    def format_timestamp_ms_rfc3339(self, timestamp_ms: int, timezone: tzinfo = DEFAULT_TZ) -> str:
        date_time_object = datetime.fromtimestamp(timestamp_ms / 1000,  tz=timezone)
        return date_time_object.isoformat()

    # This was used specifically in Ortho2 dates
    def parse_timestamp_ms_rfc3339(self, date_str: str) -> int:
        # Removing Z from the end of the timestamp
        if date_str.endswith('Z'):
            date_str = date_str[:-1]

        # Case 1 - no time zone
        if len(date_str) == 19:
            dt = datetime.fromisoformat(date_str)
            timestamp = int(dt.timestamp()) * 1000

        # Case 2 - time zone, without milliseconds
        elif len(date_str) == 25 and '.' not in date_str:
            dt = datetime.fromisoformat(date_str)
            timestamp = int(dt.timestamp()) * 1000

        # Case 3 - time zone, with milliseconds
        elif date_str[-6] in ['-', '+'] and '.' in date_str:
            datetime_str = date_str[:-6]
            timezone_str = date_str[-6:]

            datetime_base_str = datetime_str.split('.')[0]
            datetime_milliseconds_str = datetime_str.split('.')[1]
            if len(datetime_milliseconds_str) == 1:
                datetime_milliseconds_str = datetime_milliseconds_str + '00'
            elif len(datetime_milliseconds_str) == 2:
                datetime_milliseconds_str = datetime_milliseconds_str + '0'
            elif len(datetime_milliseconds_str) > 3:
                datetime_milliseconds_str = datetime_milliseconds_str[:3]

            date_str = datetime_base_str + '.' + datetime_milliseconds_str + timezone_str
            dt = datetime.fromisoformat(date_str)
            timestamp = int(dt.timestamp()) * 1000

        # Case 4 - milliseconds without timezone
        elif '.' in date_str:
            datetime_base_str = date_str.split('.')[0]
            datetime_milliseconds_str = date_str.split('.')[1]
            if len(datetime_milliseconds_str) == 1:
                datetime_milliseconds_str = datetime_milliseconds_str + '00'
            elif len(datetime_milliseconds_str) == 2:
                datetime_milliseconds_str = datetime_milliseconds_str + '0'
            elif len(datetime_milliseconds_str) > 3:
                datetime_milliseconds_str = datetime_milliseconds_str[:3]

            date_str = datetime_base_str + '.' + datetime_milliseconds_str
            dt = datetime.fromisoformat(date_str)
            timestamp = int(dt.timestamp()) * 1000

        # Invalid date
        else:
            raise RuntimeError(f"Not an RFC3339 date format! {date_str}")

        return timestamp
    #-------------------------------------------------------------------------------------------------------------------



    # Day
    #-------------------------------------------------------------------------------------------------------------------
    def get_day_start_timestamp_ms(self, year: int, month: int, day: int, timezone: tzinfo = DEFAULT_TZ) -> int:
        return self.get_timestamp_ms(year, month, day, hour=0, minute=0, second=1, timezone=timezone)

    def get_day_end_timestamp_ms(self, year: int, month: int, day: int, timezone: tzinfo = DEFAULT_TZ) -> int:
        return self.get_timestamp_ms(year, month, day, hour=23, minute=59, second=59, timezone=timezone)

    def get_day_start_end_timestamps_ms(self, year: int, month: int, day: int, timezone: tzinfo = DEFAULT_TZ) -> (int, int):
        return self.get_day_start_timestamp_ms(year, month, day, timezone=timezone), self.get_day_end_timestamp_ms(year, month, day, timezone=timezone)
    #-------------------------------------------------------------------------------------------------------------------



    # Month
    #-------------------------------------------------------------------------------------------------------------------
    def get_month_number_of_days(self, year: int, month: int) -> int:
        x, number_of_days_in_month = calendar.monthrange(year, month)
        return number_of_days_in_month

    def get_month_start_timestamp_ms(self, year: int, month: int, timezone: tzinfo = DEFAULT_TZ) -> int:
        return self.get_day_start_timestamp_ms(year, month, 1, timezone=timezone)

    def get_month_end_timestamp_ms(self, year: int, month: int, timezone: tzinfo = DEFAULT_TZ) -> int:
        number_of_days_in_month = self.get_month_number_of_days(year, month)
        return self.get_day_end_timestamp_ms(year, month, number_of_days_in_month, timezone=timezone)

    def get_month_start_end_timestamps_ms(self, year: int, month: int, timezone: tzinfo = DEFAULT_TZ) -> (int, int):
        return self.get_month_start_timestamp_ms(year, month, timezone=timezone), self.get_month_end_timestamp_ms(year, month, timezone=timezone)

    def get_month_name(self, month: int) -> str:
        return calendar.month_name[month]

    def is_timestamp_in_month(self, timestamp_ms: int, year: int, month: int, timezone: tzinfo = DEFAULT_TZ) -> bool:
        month_start_ms, month_end_ms = self.get_month_start_end_timestamps_ms(year, month, timezone=timezone)
        return month_start_ms <= timestamp_ms <= month_end_ms

    def is_timestamp_in_months(self, timestamp_ms: int, year: int, months: List[int], timezone: tzinfo = DEFAULT_TZ) -> bool:
        for month in months:
            if self.is_timestamp_in_month(timestamp_ms, year, month, timezone=timezone):
                return True
        return False
    #-------------------------------------------------------------------------------------------------------------------



    # Year
    #-------------------------------------------------------------------------------------------------------------------
    def get_year_start_timestamp_ms(self, year: int, timezone: tzinfo = DEFAULT_TZ) -> int:
        return self.get_month_start_timestamp_ms(year, 1, timezone=timezone)

    def get_year_end_timestamp_ms(self, year: int, timezone: tzinfo = DEFAULT_TZ) -> int:
        return self.get_month_end_timestamp_ms(year, 12, timezone=timezone)

    def get_year_start_end_timestamps_ms(self, year: int, timezone: tzinfo = DEFAULT_TZ) -> (int, int):
        return self.get_year_start_timestamp_ms(year, timezone=timezone), self.get_year_end_timestamp_ms(year, timezone=timezone)

    def is_timestamp_in_year(self, timestamp_ms: int, year: int, timezone: tzinfo = DEFAULT_TZ) -> bool:
        year_start_ms, year_end_ms = self.get_year_start_end_timestamps_ms(year, timezone=timezone)
        return year_start_ms <= timestamp_ms <= year_end_ms
    #-------------------------------------------------------------------------------------------------------------------

import pandas as pd

from typing import Tuple

import datetime
from dateutil.relativedelta import relativedelta


class DateRangeError(Exception):
    """This date is before the Divvy start."""


class DivvyDates:
    """Class that stores and calculates different dates associated with the Divvy Program."""

    first_date = datetime.date(2020, 4, 1)
    electric_trials = datetime.date(2020, 7, 13)
    first_electric_date = datetime.date(2020, 7, 28)
    # Last day of the west of Western pricing
    end_of_waiver = datetime.date(2022, 5, 10)

    @property
    def last_date(self) -> datetime.date:
        """Latest available day in the historical dataset."""
        return datetime.date.today().replace(day=1) - relativedelta(months=1)

    @property
    def date_range(self) -> Tuple[str, str]:
        return str(self.first_date), str(self.last_date)

    def check_valid(self, date: datetime.date) -> None:
        if date < self.first_date:
            raise DateRangeError(f"{date} is before the historical trips.")

        if date > self.last_date:
            raise DateRangeError(f"{date} data hasn't been released yet.")

    def create_date_range(self, start_date: str, end_date: str) -> list[datetime.date]:
        dates = pd.date_range(
            str(self.first_of_month(start_date)),
            str(self.first_of_month(end_date)),
            freq="MS",
        )

        return [date.to_pydatetime().date() for date in dates]

    @staticmethod
    def first_of_month(date: str) -> datetime.date:
        return datetime.datetime.strptime(date, "%Y-%m-%d").date().replace(day=1)

    @staticmethod
    def to_date(year: int, month: int) -> datetime.date:
        return datetime.date(year, month, 1)
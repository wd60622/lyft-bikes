import pandas as pd

import io
import zipfile
import requests

import datetime

from divvy.divvy_request import BadRequest
from divvy.historical.dates import DivvyDates


class Downloader:
    """Class to download historical trips."""

    def __init__(self, date: datetime.date) -> None:
        self.date = date

    def file_name(self, suffix: str) -> str:
        return f"{self.date:%Y%m}-divvy-tripdata.{suffix}"

    @property
    def url(self):
        return f"https://divvy-tripdata.s3.amazonaws.com/{self.file_name(suffix='zip')}"

    def read(self) -> pd.DataFrame:
        response = requests.get(self.url)

        if not response.ok:
            raise BadRequest(f"The response for {self.url} wasn't okay.")

        zipdata = zipfile.ZipFile(io.BytesIO(response.content))

        return pd.read_csv(zipdata.open(self.file_name(suffix="csv")))


class HistoricalTrips:
    def __init__(self):
        self.dates = DivvyDates()

    def read(self, start_date: str, end_date: str) -> pd.DataFrame:
        """Return historical trips for a given range of dates

        Args:
            start_date: start date for the data in %Y-%m-%d format
            end_date: end date in the same format

        Returns:
            Historical trip DataFrame for the date range provided.

        """
        return pd.concat(
            [
                self.get_trips(date.year, date.month)
                for date in self.dates.create_date_range(start_date, end_date)
            ],
            ignore_index=True,
        )

    def get_trips(self, year: int, month: int) -> pd.DataFrame:
        """Return pandas.DataFrame for a given year and month"""
        time = self.dates.to_date(year, month)
        self.dates.check_valid(time)

        downloader = Downloader(time)

        return downloader.read()


if __name__ == "__main__":
    trips = HistoricalTrips()
    df_trips = trips.read(start_date="2021-01-01", end_date="2021-02-01")
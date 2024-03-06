import click
import tqdm
from datetime import datetime
from time import sleep


@click.group()
@click.version_option()
def cli():
    """The command-line interface for past-time."""


@cli.command("now")
def now():
    """Show the data according the current day."""
    days = Days()
    progressbar = ProgressBar()
    progressbar.run(days.passed_days, days.total_days, days.days_till_end_year)


class Days:
    """Representation of the days."""

    def __init__(self):
        """Initialize the days."""
        self.now = datetime.now()
        self.total_days = (
            datetime(self.now.year, 12, 31) - datetime(self.now.year, 1, 1)
        ).days
        self.days_till_end_year = (datetime(self.now.year, 12, 31) - self.now).days
        self.passed_days = (self.now - datetime(self.now.year, 1, 1)).days
        self.percent_days = (self.passed_days / self.total_days) * 100


class ProgressBar:
    """Representation of a progress bar."""

    def __init__(self):
        """Initialize the progress bar."""
        self.description = "Days"
        self.unit = "days"
        self.bar = "{l_bar}{bar}|"

    def run(self, passed_days, total_days, left_days):
        """Run the progress bar."""
        for day in tqdm.trange(
            passed_days,
            total=total_days,
            unit_scale=True,
            desc=self.description,
            unit=self.unit,
            bar_format=self.bar,
        ):
            sleep(0.005)
        print(
            f"{passed_days} of {total_days} days of the year passed. {left_days} left."
        )

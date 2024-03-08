"""
Custom Exceptions Module

This module defines custom exception classes used in the project.

Classes:
    InvalidColumnNamesError: Exception raised when the invalid column names are found in the tournament schedule DataFrame.
    InvalidScheduleDataError: Exception raised when the input schedule dataframe is invalid.
    NoQualifyingScenariosError: Exception raised when no qualifying scenarios are found for the given team.
    TeamNotFoundError: Exception raised when the team is not found in the tournament schedule.
    TournamentCompletionBelowCutoffError: Exception raised when the percentage of tournament completion is below the specified cutoff.
"""


class InvalidColumnNamesError(ValueError):
    """
    Custom error class for invalid column names in the tournament schedule DataFrame.
    """

    def __init__(self, column_name):
        self.column_name = column_name
        super().__init__(f"{column_name} is not found in tournament_schedule columns")


class InvalidScheduleDataError(ValueError):
    """Exception raised when the input schedule dataframe is invalid."""

    def __init__(self, message="Invalid schedule data"):
        self.message = message
        super().__init__(self.message)


class NoQualifyingScenariosError(Exception):
    """Exception raised when no qualifying scenarios are found for the given team."""

    def __init__(self, message="No qualifying scenarios found"):
        self.message = message
        super().__init__(self.message)


class TeamNotFoundError(Exception):
    """Exception raised when the team is not found in the tournament schedule."""

    def __init__(self, message="Team not found in tournament schedule"):
        self.message = message
        super().__init__(self.message)


class TournamentCompletionBelowCutoffError(Exception):
    """Exception raised when the percentage of tournament completion is below the specified cutoff."""

    def __init__(self, message="Percentage of tournament completion is below the specified cutoff."):
        self.message = message
        super().__init__(self.message)

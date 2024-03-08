"""
points_table_simulator

A package for calculating points tables for tournaments based on provided schedules and points systems and simulating the various qualification 
    scenario for a given team in the course of the tournament.

This package provides a PointsTableSimulator class that allows users to simulate and calculate points tables for tournaments. 
    The class enables users to input tournament schedules, points awarded for different match outcomes (wins, draws, and no results), 
    and then provides methods to calculate the current points table and simulate qualification scenarios for teams.

Example:
    To use this package, you can instantiate the PointsTableSimulator class with the tournament schedule and points system details:

    ```python
    from points_table_simulator import PointsTableSimulator
    import pandas as pd

    # Load the tournament schedule DataFrame
    tournament_schedule = pd.read_csv("tournament_schedule.csv")

    # Note: The tournament schedule DataFrame should have the following columns:
    #   - "match_number" column containing the match number
    #   - "home" column containing the home team names
    #   - "away" column containing the away team names
    #   - "winner" column containing the match result (winning_team_name, draw, or no result)
    # If the tournament schedule DataFrame contains different names than this, you can use arguments in PointsTableSimulator class to
    # specify the column names. 


    # Instantiate the PointsTableSimulator object
    simulator = PointsTableSimulator(
        tournament_schedule=tournament_schedule,
        points_for_a_win=3,
        points_for_a_no_result=1,
        points_for_a_draw=1
    )

    # Calculate the current points table
    current_table = simulator.current_points_table()

    # Simulate qualification scenarios for a specific team
    qualification_tables, qualification_match_results = simulator.simulate_the_qualification_scenarios(
        team_name="Team A",
        top_x_position_in_the_table=4,
        desired_number_of_scenarios=5
    )
    ```

Author:
    Nishanth Muruganantham
    email: nishanthmurugananth10@gmail.com

"""

import itertools
from typing import Dict, List, Tuple
import pandas as pd
from points_table_simulator.constants import (
    TOURNAMENT_COMPLETION_CUTOFF_PERCENTAGE
)
from points_table_simulator.exceptions import (
    InvalidColumnNamesError,
    InvalidScheduleDataError,
    NoQualifyingScenariosError,
    TeamNotFoundError,
    TournamentCompletionBelowCutoffError
)


class PointsTableSimulator:     # pylint: disable = too-many-instance-attributes

    """
    PointsTableSimulator

    A class for simulating and calculating points table for a tournament based on provided schedule and points system.

    Args:
        tournament_schedule (pd.DataFrame): DataFrame containing the schedule of the tournament matches.
        points_for_a_win (int): Points awarded for a win.
        points_for_a_no_result (int, optional): Points awarded for a match with no result. Default is 1.
        points_for_a_draw (int, optional): Points awarded for a draw. Default is 1.
        tournament_schedule_away_team_column_name (str, optional): Name of the column in the schedule DataFrame
            containing the away team names. Default is "away".
        tournament_schedule_home_team_column_name (str, optional): Name of the column in the schedule DataFrame
            containing the home team names. Default is "home".
        tournament_schedule_match_number_column_name (str, optional): Name of the column in the schedule DataFrame
            containing the match numbers. Default is "match_number".
        tournament_schedule_winning_team_column_name (str, optional): Name of the column in the schedule DataFrame
            containing the winning team names. Default is "winner".

    Attributes:
        tournament_schedule (pd.DataFrame): DataFrame containing the schedule of the tournament matches.
        points_for_a_win (int): Points awarded for a win.
        points_for_a_no_result (int): Points awarded for a match with no result.
        points_for_a_draw (int): Points awarded for a draw.
        tournament_schedule_away_team_column_name (str): Name of the column in the schedule DataFrame
            containing the away team names.
        tournament_schedule_home_team_column_name (str): Name of the column in the schedule DataFrame
            containing the home team names.
        tournament_schedule_match_number_column_name (str): Name of the column in the schedule DataFrame
            containing the match numbers.
        tournament_schedule_winning_team_column_name (str): Name of the column in the schedule DataFrame
            containing the winning team names.

    Methods:
        current_points_table(): Calculates the current points table based on the provided tournament schedule.
        simulate_the_qualification_scenarios(): Finds qualification scenarios for a specified team to reach the desired position in the points table.
    """

    def __init__(       # pylint: disable = too-many-arguments
        self,
        tournament_schedule: pd.DataFrame,
        points_for_a_win: int,
        points_for_a_no_result: int = 1,
        points_for_a_draw: int = 1,
        tournament_schedule_away_team_column_name: str = "away",
        tournament_schedule_home_team_column_name: str = "home",
        tournament_schedule_match_number_column_name: str = "match_number",
        tournament_schedule_winning_team_column_name: str = "winner",
    ) -> None:
        """
        Initializes PointsTableSimulator object with provided parameters.

        Args:
            tournament_schedule (pd.DataFrame): DataFrame containing the schedule of the tournament matches.
            points_for_a_win (int): Points awarded for a win.
            points_for_no_result (int, optional): Points awarded for a match with no result. Default is 1.
            points_for_a_draw (int, optional): Points awarded for a draw. Default is 1.
            tournament_schedule_away_team_column_name (str, optional): Name of the column in the schedule DataFrame
                containing the away team names. Default is "away".
            tournament_schedule_home_team_column_name (str, optional): Name of the column in the schedule DataFrame
                containing the home team names. Default is "home".
            tournament_schedule_match_number_column_name (str, optional): Name of the column in the schedule DataFrame
                containing the match numbers. Default is "match_number".
            tournament_schedule_winning_team_column_name (str, optional): Name of the column in the schedule DataFrame
                containing the winning team names. Default is "winner".
        """
        self._validate_input_types(
            tournament_schedule,
            points_for_a_win,
            points_for_a_no_result,
            points_for_a_draw,
            tournament_schedule_away_team_column_name=tournament_schedule_away_team_column_name,
            tournament_schedule_home_team_column_name=tournament_schedule_home_team_column_name,
            tournament_schedule_match_number_column_name=tournament_schedule_match_number_column_name,
            tournament_schedule_winning_team_column_name=tournament_schedule_winning_team_column_name
        )
        self.tournament_schedule: pd.DataFrame = tournament_schedule
        self.points_for_a_draw: int = points_for_a_draw
        self.points_for_a_no_result: int = points_for_a_no_result
        self.points_for_a_win: int = points_for_a_win
        self.tournament_schedule_away_team_column_name: str = tournament_schedule_away_team_column_name
        self.tournament_schedule_home_team_column_name: str = tournament_schedule_home_team_column_name
        self.tournament_schedule_match_number_column_name: str = tournament_schedule_match_number_column_name
        self.tournament_schedule_winning_team_column_name: str = tournament_schedule_winning_team_column_name
        self._validate_schedule_dataframe_columns()
        self._validate_schedule_dataframe_data()

    @property
    def current_points_table(self) -> pd.DataFrame:
        """
        Calculates the current points table based on the provided tournament schedule.

        Returns:
            pd.DataFrame: DataFrame containing the current points table with the following columns:
                - 'team': The name of the team.
                - 'matches_played': The total number of matches played by the team.
                - 'matches_won': The total number of matches won by the team.
                - 'matches_lost': The total number of matches lost by the team.
                - 'matches_drawn': The total number of matches drawn by the team.
                - 'matches_with_no_result': The total number of matches with no result for the team.
                - 'remaining_matches': The total number of remaining matches for the team.
                - 'points': The total points earned by the team based on wins, draws, and no results.
        """

        team_points_data: List = []

        teams: set = set(self.tournament_schedule[self.tournament_schedule_away_team_column_name].unique()).union(
            set(self.tournament_schedule[self.tournament_schedule_home_team_column_name].unique())
        )

        for team in teams:
            matches_played: int = len(self.tournament_schedule[
                (
                    (self.tournament_schedule[self.tournament_schedule_away_team_column_name] == team) |
                    (self.tournament_schedule[self.tournament_schedule_home_team_column_name] == team)
                ) &
                (
                    (self.tournament_schedule[self.tournament_schedule_winning_team_column_name].fillna("") != "")
                )
            ])

            matches_won: int = len(self.tournament_schedule[
                (self.tournament_schedule[self.tournament_schedule_winning_team_column_name] == team)
            ])

            matches_lost: int = len(self.tournament_schedule[
                (
                    (self.tournament_schedule[self.tournament_schedule_away_team_column_name] == team) |
                    (self.tournament_schedule[self.tournament_schedule_home_team_column_name] == team)
                ) &
                (
                    (self.tournament_schedule[self.tournament_schedule_winning_team_column_name] != team) &
                    (self.tournament_schedule[self.tournament_schedule_winning_team_column_name].fillna("") != "")
                )
            ])

            matches_drawn: int = len(self.tournament_schedule[
                ((self.tournament_schedule[self.tournament_schedule_away_team_column_name] == team) |
                (self.tournament_schedule[self.tournament_schedule_home_team_column_name] == team)) &
                (self.tournament_schedule[self.tournament_schedule_winning_team_column_name] == "Draw")
            ])

            matches_with_no_result: int = len(self.tournament_schedule[
                ((self.tournament_schedule[self.tournament_schedule_away_team_column_name] == team) |
                (self.tournament_schedule[self.tournament_schedule_home_team_column_name] == team)) &
                (self.tournament_schedule[self.tournament_schedule_winning_team_column_name] == "No Result")
            ])

            remaining_matches: int = len(self.tournament_schedule[
                (
                    (self.tournament_schedule[self.tournament_schedule_away_team_column_name] == team) |
                    (self.tournament_schedule[self.tournament_schedule_home_team_column_name] == team)
                ) &
                (
                    (self.tournament_schedule[self.tournament_schedule_winning_team_column_name].fillna("") == "")
                )
            ])

            points: int = (matches_won * self.points_for_a_win) + (matches_drawn * self.points_for_a_draw) + \
                (matches_with_no_result * self.points_for_a_no_result)

            team_points_data.append({
                "team": team,
                "matches_played": matches_played,
                "matches_won": matches_won,
                "matches_lost": matches_lost,
                "matches_drawn": matches_drawn,
                "matches_with_no_result": matches_with_no_result,
                "remaining_matches": remaining_matches,
                "points": points
            })

        current_points_table = pd.DataFrame(team_points_data)
        current_points_table.sort_values(by="points", ascending=False, inplace=True)
        current_points_table.reset_index(drop=True, inplace=True)

        return current_points_table

    def simulate_the_qualification_scenarios(
        self, team_name: str, top_x_position_in_the_table: int, desired_number_of_scenarios: int = 3
    ) -> Tuple[List[pd.DataFrame], List[pd.DataFrame]]:
        """
        Finds qualification scenarios for a specified team to reach the desired position in the points table.

        This function simulates various match result scenarios for the remaining matches in the tournament schedule
        to determine the combinations that would enable the specified team to qualify within the top X positions
        in the points table.

        Args:
            team (str): The name of the team for which qualification scenarios are being determined.
            top_x_position (int): The desired position in the points table for qualification.
            desired_number_of_scenarios (int): The desired number of qualifying scenarios to find.

        Returns:
            Tuple[List[pd.DataFrame], List[pd.DataFrame]]: A tuple containing two lists:
                - List[pd.DataFrame]: List of points tables for qualification scenarios.
                - List[pd.DataFrame]: List of remaining_match_outcome for qualification scenarios.

        The function iterates through all possible combinations of match results for the remaining matches
        in the tournament schedule. For each combination, it calculates the updated points table and checks
        if the specified team qualifies within the top X positions. Once enough qualifying scenarios are found
        based on the desired number of scenarios, the function stops iterating and returns the results.

        Example:
            qualification_tables, qualification_match_results = find_qualification_scenarios(
                team="Team A",
                top_x_position=4,
                desired_number_of_scenarios=5
            )
            for i in range(len(qualification_tables)):
                print(f"Qualification Scenario {i+1}:")
                print(qualification_tables[i])
                print("Match Results:")
                print(qualification_match_results[i])
                print("\n")
        """

        self._validate_the_inputs_for_simulate_qualification_scenarios(
            team_name, top_x_position_in_the_table, desired_number_of_scenarios
        )
        list_of_points_tables_for_qualification_scenarios = []
        list_of_remaining_match_result_for_qualification_scenarios = []

        remaining_matches_in_the_schedule = self._find_remaining_matches_in_the_schedule()
        number_of_completed_matches: int = len(self.tournament_schedule) - len(remaining_matches_in_the_schedule)
        remaining_schedule_df: pd.DataFrame = self.tournament_schedule.iloc[
            number_of_completed_matches:, :
        ]

        initial_points_table = self.current_points_table

        for possible_results_for_remaining_matches in itertools.product(*remaining_matches_in_the_schedule):
            temporary_schedule_df = remaining_schedule_df.copy()
            updated_points_table = initial_points_table.copy()

            for match_number, possible_winning_team in enumerate(possible_results_for_remaining_matches):
                home_team, away_team = remaining_matches_in_the_schedule[match_number]
                temporary_schedule_df.loc[
                    number_of_completed_matches + match_number,
                    self.tournament_schedule_winning_team_column_name
                ] = possible_winning_team
                updated_points_table = self._update_points_table(
                    updated_points_table, home_team, away_team, possible_winning_team
                )

            updated_points_table.sort_values(by="points", ascending=False, inplace=True)
            updated_points_table.reset_index(drop=True, inplace=True)

            if team_name in updated_points_table["team"].values[:top_x_position_in_the_table]:
                list_of_points_tables_for_qualification_scenarios.append(updated_points_table)
                list_of_remaining_match_result_for_qualification_scenarios.append(temporary_schedule_df)

            if len(list_of_points_tables_for_qualification_scenarios) >= desired_number_of_scenarios:
                break

        if not list_of_points_tables_for_qualification_scenarios:
            raise NoQualifyingScenariosError(
                f"No qualifying scenarios found for the team '{team_name}' in the top '{top_x_position_in_the_table}' positions."
            )

        return list_of_points_tables_for_qualification_scenarios, list_of_remaining_match_result_for_qualification_scenarios

    def _find_remaining_matches_in_the_schedule(self) -> List[Tuple[str, str]]:
        remaining_matches_df = self.tournament_schedule[
            self.tournament_schedule[self.tournament_schedule_winning_team_column_name].fillna("") == ""
        ]
        remaining_matches = list(remaining_matches_df.apply(
            lambda row: (row[self.tournament_schedule_home_team_column_name], row[self.tournament_schedule_away_team_column_name]),
            axis=1
        ))
        total_matches_in_the_schedule = len(self.tournament_schedule)
        completed_matches = total_matches_in_the_schedule - len(remaining_matches)
        tournament_completion_percentage = (completed_matches / total_matches_in_the_schedule) * 100
        if tournament_completion_percentage < TOURNAMENT_COMPLETION_CUTOFF_PERCENTAGE:
            raise TournamentCompletionBelowCutoffError(
                f"This utility cannot be used at this stage, since the tournament completion percentage is {tournament_completion_percentage:.2f}%, \
                    which is below the cutoff percentage of {TOURNAMENT_COMPLETION_CUTOFF_PERCENTAGE}%."
            )
        return remaining_matches

    def _update_points_table(
        self, points_table: pd.DataFrame, home_team: str, away_team: str, winning_team: str
    ) -> pd.DataFrame:
        points_table.loc[points_table["team"] == winning_team, "matches_won"] += 1
        points_table.loc[points_table['team'] == winning_team, 'points'] += self.points_for_a_win
        points_table.loc[points_table['team'] == home_team, 'matches_played'] += 1
        points_table.loc[points_table['team'] == away_team, 'matches_played'] += 1
        return points_table

    @staticmethod
    def _validate_input_types(
        tournament_schedule: pd.DataFrame,
        points_for_a_win: int,
        points_for_a_no_result: int,
        points_for_a_draw: int,
        **kwargs
    ):
        """
        Validates the types of input arguments.

        Args:
            tournament_schedule (pd.DataFrame): DataFrame containing the schedule of the tournament matches.
            points_for_a_win (int): Points awarded for a win.
            points_for_no_result (int): Points awarded for a match with no result.
            points_for_a_draw (int): Points awarded for a draw.
            tournament_schedule_away_team_column_name (str): Name of the column in the schedule DataFrame
                containing the away team names.
            tournament_schedule_home_team_column_name (str): Name of the column in the schedule DataFrame
                containing the home team names.
            tournament_schedule_match_number_column_name (str): Name of the column in the schedule DataFrame
                containing the match numbers.
            tournament_schedule_winning_team_column_name (str): Name of the column in the schedule DataFrame
                containing the winning team names.

        Raises:
            TypeError: If any of the input arguments have incorrect types.
        """
        type_map = {
            "tournament_schedule": (tournament_schedule, pd.DataFrame),
            "points_for_a_win": (points_for_a_win, int),
            "points_for_a_no_result": (points_for_a_no_result, int),
            "points_for_a_draw": (points_for_a_draw, int),
        }

        for arg_name, (arg_value, expected_type) in type_map.items():
            if not isinstance(arg_value, expected_type):
                raise TypeError(f"'{arg_name}' must be a '{expected_type}'")
        for key, value in kwargs.items():
            if not isinstance(value, str):
                raise TypeError(f"'{key}' must be a '{str}'")

    def _validate_schedule_dataframe_columns(self):
        """
        Validates whether the provided column names are matching with the tournament_schedule DataFrame.

        Raises:
            ValueError: If any provided column name is missing from the columns of tournament_schedule dataframe.
        """
        _column_map: Dict[str, str] = {
            "tournament_schedule_away_team_column_name": self.tournament_schedule_away_team_column_name,
            "tournament_schedule_home_team_column_name": self.tournament_schedule_home_team_column_name,
            "tournament_schedule_match_number_column_name": self.tournament_schedule_match_number_column_name,
            "tournament_schedule_winning_team_column_name": self.tournament_schedule_winning_team_column_name,
        }
        schedule_dataframe_columns = self.tournament_schedule.columns
        for column_name, column_value in _column_map.items():
            if column_value not in schedule_dataframe_columns:
                raise InvalidColumnNamesError(f"{column_name} '{column_value}' is not found in given tournament_schedule columns")

    def _validate_schedule_dataframe_data(self):
        for column in (
            self.tournament_schedule_away_team_column_name,
            self.tournament_schedule_home_team_column_name,
            self.tournament_schedule_match_number_column_name,
        ):
            if bool(self.tournament_schedule[column].isnull().any()):
                raise InvalidScheduleDataError(
                    f"the given schedule contains rows with empty values or NaN in the {column} column"
                )

    def _validate_the_inputs_for_simulate_qualification_scenarios(
        self, team_name: str, top_x_position_in_the_table: int, desired_number_of_scenarios: int
    ):
        _type_map: Dict[str, type] = {
            "team_name": str,
            "top_x_position_in_the_table": int,
            "desired_number_of_scenarios": int,
        }
        for key, value in _type_map.items():
            if not isinstance(locals()[key], value):
                raise TypeError(f"'{key}' must be a '{value}'")
        if desired_number_of_scenarios <= 0:
            raise ValueError("'desired_number_of_scenarios' must be greater than 0")
        if top_x_position_in_the_table <= 0:
            raise ValueError("'top_x_position_in_the_table' must be greater than 0")
        if team_name not in self.current_points_table["team"].values:
            raise TeamNotFoundError(f"'{team_name}' is not found in the current points table or in the given schedule")
        if top_x_position_in_the_table > len(self.current_points_table):
            raise ValueError(
                "'top_x_position_in_the_table' must be less than or equal to the number of teams in the table"
            )

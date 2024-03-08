from unittest import TestCase
import pandas as pd
from points_table_simulator.exceptions import (
    InvalidColumnNamesError,
    InvalidScheduleDataError,
    NoQualifyingScenariosError,
    TeamNotFoundError,
    TournamentCompletionBelowCutoffError
)
from points_table_simulator.points_table_simulator import PointsTableSimulator


class ErrorTests(TestCase):

    """
        This class contains tests for the errors raised by the PointsTableSimulator class. It covers both default exceptions and custom exceptions.
    """

    def test_when_wrong_types_are_given_as_inputs_then_raise_type_error(self):
        """
            This test checks that the PointsTableSimulator class raises a TypeError when the wrong types of inputs are
            given to the constructor.
        """
        tournament_schedule = "dataframe"
        expected_error_message = f"'tournament_schedule' must be a '{pd.DataFrame}'"
        with self.assertRaises(TypeError) as exception:
            PointsTableSimulator(tournament_schedule, points_for_a_win=3)
        self.assertEqual(str(exception.exception), expected_error_message)

    def test_WHEN_wrong_types_are_given_as_input_column_names_THEN_raise_TYPE_ERROR(self):
        """
            This test checks that the PointsTableSimulator class raises a TypeError, when the wrong column_name types are
            given to the constructor.
        """
        tournament_schedule = pd.DataFrame({
            "match_number": list(range(1, 7)),
            "home": ["Team A", "Team B", "Team C", "Team A", "Team B", "Team C"],
            "away": ["Team B", "Team C", "Team A", "Team C", "Team A", "Team B"],
            "winner": ["Team A", "Team C", "Team A", "Team C", "Team A", "Team B"]
        })
        expected_error_message = f"'tournament_schedule_home_team_column_name' must be a '{str}'"

        with self.assertRaises(TypeError) as exception:
            PointsTableSimulator(tournament_schedule, points_for_a_win=3, tournament_schedule_home_team_column_name=3)
        self.assertEqual(str(exception.exception), expected_error_message)

    def test_WHEN_wrong_types_are_given_as_input_for_simulate_qualification_scenario_function_THEN_raise_Type_Error(self):
        """
            This test checks that the PointsTableSimulator class raises a TypeError, when the wrong types of inputs are
            given to the simulate_qualification_scenario function.
        """
        tournament_schedule = pd.DataFrame({
            "match_number": list(range(1, 7)),
            "home": ["Team A", "Team B", "Team C", "Team A", "Team B", "Team C"],
            "away": ["Team B", "Team C", "Team A", "Team C", "Team A", "Team B"],
            "winner": ["Team A", "Team C", "Team A", "Team C", "Team A", None]
        })
        expected_error_message = f"'team_name' must be a '{str}'"
        simulator = PointsTableSimulator(tournament_schedule, points_for_a_win=3)

        with self.assertRaises(TypeError) as exception:
            simulator.simulate_the_qualification_scenarios(team_name=3, top_x_position_in_the_table=2)
        self.assertEqual(str(exception.exception), expected_error_message)

    def test_WHEN_number_of_scenarios_are_given_as_non_positive_for_simulate_qualification_scenario_function_THEN_raise_Value_Error(self):
        """
            This test checks that the PointsTableSimulator class raises a ValueError, when the non-positive number of
            scenarios are given to the simulate_qualification_scenario function.
        """
        tournament_schedule = pd.DataFrame({
            "match_number": list(range(1, 7)),
            "home": ["Team A", "Team B", "Team C", "Team A", "Team B", "Team C"],
            "away": ["Team B", "Team C", "Team A", "Team C", "Team A", "Team B"],
            "winner": ["Team A", "Team C", "Team A", "Team C", "Team A", None]
        })
        expected_error_message = "'desired_number_of_scenarios' must be greater than 0"
        simulator = PointsTableSimulator(tournament_schedule, points_for_a_win=3)

        with self.assertRaises(ValueError) as exception:
            simulator.simulate_the_qualification_scenarios(
                team_name="Team A", top_x_position_in_the_table=2, desired_number_of_scenarios=0
            )
        self.assertEqual(str(exception.exception), expected_error_message)

    def test_WHEN_top_x_position_in_the_table_is_given_as_non_positive_for_simulate_qualification_scenario_function_THEN_raise_Value_Error(self):
        """
            This test checks that the PointsTableSimulator class raises a ValueError, when the non-positive top_x_position_in_the_table
            is given to the simulate_qualification_scenario function.
        """
        tournament_schedule = pd.DataFrame({
            "match_number": list(range(1, 7)),
            "home": ["Team A", "Team B", "Team C", "Team A", "Team B", "Team C"],
            "away": ["Team B", "Team C", "Team A", "Team C", "Team A", "Team B"],
            "winner": ["Team A", "Team C", "Team A", "Team C", "Team A", None]
        })
        expected_error_message = "'top_x_position_in_the_table' must be greater than 0"
        simulator = PointsTableSimulator(tournament_schedule, points_for_a_win=3)

        with self.assertRaises(ValueError) as exception:
            simulator.simulate_the_qualification_scenarios(
                team_name="Team A", top_x_position_in_the_table=-2, desired_number_of_scenarios=2
            )
        self.assertEqual(str(exception.exception), expected_error_message)

    def test_WHEN_top_x_position_in_the_table_is_greater_then_the_number_of_teams_for_simulate_qualification_scenario_function_THEN_raise_Value_Error(self):
        """
            This test checks that the PointsTableSimulator class raises a ValueError, when the top_x_position_in_the_table
            is greater than the number of teams available in the given schedule.
        """
        tournament_schedule = pd.DataFrame({
            "match_number": list(range(1, 7)),
            "home": ["Team A", "Team B", "Team C", "Team A", "Team B", "Team C"],
            "away": ["Team B", "Team C", "Team A", "Team C", "Team A", "Team B"],
            "winner": ["Team A", "Team C", "Team A", "Team C", "Team A", None]
        })
        expected_error_message = "'top_x_position_in_the_table' must be less than or equal to the number of teams in the table"
        simulator = PointsTableSimulator(tournament_schedule, points_for_a_win=3)

        with self.assertRaises(ValueError) as exception:
            simulator.simulate_the_qualification_scenarios(
                team_name="Team A", top_x_position_in_the_table=12, desired_number_of_scenarios=2
            )
        self.assertEqual(str(exception.exception), expected_error_message)

    def test_WHEN_number_of_scenarios_is_given_as_non_positive_for_simulate_qualification_scenario_function_THEN_raise_Value_Error(self):
        """
            This test checks that the PointsTableSimulator class raises a ValueError, when the non-positive number of
            scenarios are given to the simulate_qualification_scenario function.
        """
        tournament_schedule = pd.DataFrame({
            "match_number": list(range(1, 7)),
            "home": ["Team A", "Team B", "Team C", "Team A", "Team B", "Team C"],
            "away": ["Team B", "Team C", "Team A", "Team C", "Team A", "Team B"],
            "winner": ["Team A", "Team C", "Team A", "Team C", "Team A", None]
        })
        expected_error_message = "'desired_number_of_scenarios' must be greater than 0"
        simulator = PointsTableSimulator(tournament_schedule, points_for_a_win=3)

        with self.assertRaises(ValueError) as exception:
            simulator.simulate_the_qualification_scenarios(
                team_name="Team A", top_x_position_in_the_table=2, desired_number_of_scenarios=0
            )
        self.assertEqual(str(exception.exception), expected_error_message)

    def test_WHEN_wrong_team_is_given_for_simulate_qualification_scenario_function_THEN_raise_TeamNotFoundError(self):
        """
            This test checks that the PointsTableSimulator class raises a TeamNotFoundError, when the wrong team name is
            given to the simulate_qualification_scenario function.
        """
        wrong_team = "Team Z"
        tournament_schedule = pd.DataFrame({
            "match_number": list(range(1, 7)),
            "home": ["Team A", "Team B", "Team C", "Team A", "Team B", "Team C"],
            "away": ["Team B", "Team C", "Team A", "Team C", "Team A", "Team B"],
            "winner": ["Team A", "Team C", "Team A", "Team C", "Team A", None]
        })
        expected_error_message = f"'{wrong_team}' is not found in the current points table or in the given schedule"
        simulator = PointsTableSimulator(tournament_schedule, points_for_a_win=3)

        with self.assertRaises(TeamNotFoundError) as exception:
            simulator.simulate_the_qualification_scenarios(
                team_name=wrong_team, top_x_position_in_the_table=2, desired_number_of_scenarios=2
            )
        self.assertEqual(str(exception.exception), expected_error_message)

    def test_WHEN_column_names_are_given_different_from_the_column_names_in_given_schedule_df_THEN_raise_InvalidColumnNamesError(self):
        """
            This test checks that the PointsTableSimulator class raises a InvalidColumnNamesError, when the column names
            are given different from the column names in the given schedule df.
        """
        tournament_schedule = pd.DataFrame({
            "match_number": list(range(1, 7)),
            "home": ["Team A", "Team B", "Team C", "Team A", "Team B", "Team C"],
            "away": ["Team B", "Team C", "Team A", "Team C", "Team A", "Team B"],
            "winner": ["Team A", "Team C", "Team A", "Team C", "Team A", "Team B"]
        })

        with self.assertRaises(InvalidColumnNamesError):
            PointsTableSimulator(tournament_schedule, points_for_a_win=3, tournament_schedule_away_team_column_name="away2")

    def test_WHEN_mandatory_column_having_NaN_values_THEN_raise_InvalidScheduleDataError(self):
        """
            This test checks that the PointsTableSimulator class raises a InvalidScheduleDataError, when the mandatory
            column having NaN values.
        """
        tournament_schedule = pd.DataFrame({
            "match_number": list(range(1, 7)),
            "home": ["Team A", "Team B", "Team C", None, "Team B", "Team C"],
            "away": ["Team B", "Team C", "Team A", "Team C", "Team A", "Team B"],
            "winner": ["Team A", "Team C", None, None, None, None]
        })

        with self.assertRaises(InvalidScheduleDataError):
            PointsTableSimulator(tournament_schedule, points_for_a_win=3)

    def test_WHEN_no_qualification_scenario_found_for_given_team_into_given_position_THEN_raise_NoQualifyingScenariosError(self):
        """
            This test checks that the PointsTableSimulator class raises a NoQualifyingScenariosError, when no
            qualifying scenarios are found for the given team into the given position.
        """
        tournament_schedule = pd.DataFrame({
            "match_number": list(range(1, 7)),
            "home": ["Team A", "Team B", "Team C", "Team A", "Team B", "Team C"],
            "away": ["Team B", "Team C", "Team A", "Team C", "Team A", "Team B"],
            "winner": ["Team A", "Team C", "Team A", "Team C", "Team A", None]
        })
        simulator = PointsTableSimulator(tournament_schedule, points_for_a_win=3)

        with self.assertRaises(NoQualifyingScenariosError):
            simulator.simulate_the_qualification_scenarios("Team B", top_x_position_in_the_table=2)

    def test_simulate_the_qualification_scenarios_function_with_completed_matches_below_cutoff_THEN_raise_TournamentCompletionBelowCutoffError(self):
        """
            This test checks that the PointsTableSimulator class raises a TournamentCompletionBelowCutoffError, when
            the number of completed matches in the tournament is below the cutoff. here the cutoff is 75%

            In this test, the total league matches are 6 and only 3 are completed, which is 50% of tournamenet is completed. Therefore, the
            TournamentCompletionBelowCutoffError should be raised.
        """
        tournament_schedule = pd.DataFrame({
            "match_number": list(range(1, 7)),
            "home": ["Team A", "Team B", "Team C", "Team A", "Team B", "Team C"],
            "away": ["Team B", "Team C", "Team A", "Team C", "Team A", "Team B"],
            "winner": ["Team A", "Team C", None, None, None, None]  # Four matches remaining
        })
        simulator = PointsTableSimulator(tournament_schedule, points_for_a_win=3)

        with self.assertRaises(TournamentCompletionBelowCutoffError):
            simulator.simulate_the_qualification_scenarios("Team A", top_x_position_in_the_table=2)

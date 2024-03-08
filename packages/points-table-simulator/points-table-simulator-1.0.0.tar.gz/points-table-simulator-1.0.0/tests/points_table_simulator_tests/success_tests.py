import os
from unittest import TestCase
import pandas as pd
from points_table_simulator.points_table_simulator import PointsTableSimulator


class SuccessTests(TestCase):

    test_data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

    def test_simulate_the_qualification_scenarios_function_with_psl_2024_fixture(self):
        schedule_file = os.path.join(self.test_data_folder, 'psl_2024_fixture.csv')
        tournament_schedule = pd.read_csv(schedule_file)

        simulator = PointsTableSimulator(
            tournament_schedule, 
            points_for_a_win=2,
            tournament_schedule_away_team_column_name="Away",
            tournament_schedule_home_team_column_name="Home",
            tournament_schedule_winning_team_column_name="Winner",
            tournament_schedule_match_number_column_name="Match No"
        )

        (
            list_of_points_table_for_different_qualification_scenarios,
            list_of_remaining_match_results_for_different_qualification_scenarios
        ) = simulator.simulate_the_qualification_scenarios("Karachi Kings", top_x_position_in_the_table=4)

        self.assertEqual(len(list_of_points_table_for_different_qualification_scenarios), 3)
        self.assertEqual(len(list_of_remaining_match_results_for_different_qualification_scenarios), 3)

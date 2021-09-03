from DataGenerators.schedule_updator import get_daily_schedule
from DataGenerators.scipt_execution import record_script_execution
from DataGenerators.live_data_generator import get_live_data
from DataGenerators.players_generator import get_new_players
from DataGenerators.boxscore_generator import get_boxscore
from DataGenerators.data_to_production import data_to_production
from ETL.etl_create_gim_model_sequences import create_gim_model_sequences
from ETL.etl_consolidate_gim_values import get_new_consolidated_gims
from ETL.etl_create_gim_values import create_gim_values
from SQLCode.execute_stored_procedure import execute_proc
from ETL.etl_game_outcome_prediction import get_game_outcome_predictions


def main():
    # Downloading data
    if get_daily_schedule() == -1:
        return -1
    record_script_execution('get_daily_schedule')
    if get_live_data() == -1:
        return -1
    record_script_execution('get_live_data')
    if get_boxscore() == -1:
        return -1
    record_script_execution('get_boxscore')
    if get_new_players() == -1:
        return -1
    record_script_execution('get_new_players')

    # ETLs
    if create_gim_model_sequences() == -1:
        return -1
    record_script_execution('create_gim_model_sequences')

    if create_gim_values() == -1:
        return -1
    record_script_execution('create_gim_values')

    if get_new_consolidated_gims() == -1:
        return -1
    record_script_execution('get_new_consolidated_gims')

    if execute_proc("sp_game_prediction_team_stats_view") == -1:
        return -1
    record_script_execution('sp_game_prediction_team_stats_view')

    if get_game_outcome_predictions() == -1:
        return -1
    record_script_execution('get_game_outcome_predictions')

    # if predict_game_outcome() == -1:
    #     return -1
    # record_script_execution('create_predicting_win_model_input')

    data_to_production()


if __name__ == '__main__':
    main()

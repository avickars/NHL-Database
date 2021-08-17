from DataGenerators.schedule_updator import get_daily_schedule
from DataGenerators.scipt_execution import record_script_execution
from DataGenerators.live_data_generator import get_live_data
from DataGenerators.players_generator import get_new_players
from DataGenerators.boxscore_generator import get_boxscore
from DataGenerators.data_to_production import data_to_production
from ETL.etl_sequences import create_gim_model_input
from ETL.etl_gim_value import create_gim_values


def main():
    # # Downloading data
    # if get_daily_schedule() == -1:
    #     return -1
    # record_script_execution('get_daily_schedule')
    # if get_live_data() == -1:
    #     return -1
    # record_script_execution('get_live_data')
    # if get_boxscore() == -1:
    #     return -1
    # record_script_execution('get_boxscore')
    # if get_new_players() == -1:
    #     return -1
    # record_script_execution('get_new_players')

    # ETLs
    # if create_gim_model_input() == -1:
    #     return -1
    # record_script_execution('create_gim_model_input')
    if create_gim_values() == -1:
        return -1
    # record_script_execution('create_gim_values')



    # data_to_production()



if __name__ == '__main__':
    main()

from DataGenerators.schedule_updator import get_daily_schedule
from DataGenerators.scipt_execution import record_script_execution
from DataGenerators.live_data_generator import get_live_data
from DataGenerators.players_generator import get_new_players
from DataGenerators.boxscore_generator import get_boxscore


def main():
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
    if get_new_backup() == -1:
        return -1
    record_script_execution('get_new_backup')
    if upload_backup() == -1:
        return -1
    record_script_execution('upload_backup')





if __name__ == '__main__':
    main()

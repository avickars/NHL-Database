from DataGenerators.players_generator import update_players
from DataGenerators.scipt_execution import record_script_execution
from DataGenerators.backup_generator import upload_backup, get_new_backup


def main():
    # if update_players() == -1:
    #     return -1
    # record_script_execution('update_players')
    if get_new_backup() == -1:
        return -1
    record_script_execution('get_new_backup')
    if upload_backup() == -1:
        return -1
    record_script_execution('upload_backup')


if __name__ == '__main__':
    main()

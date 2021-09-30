from DataGenerators.players_generator import update_players
from DataGenerators.scipt_execution import record_script_execution
from DataGenerators.backup_generator import get_new_backup_usb, get_new_backup_ssd


def main():
    if update_players() == -1:
        return -1
    record_script_execution('update_players')
    if get_new_backup_usb() == -1:
        return -1
    record_script_execution('get_new_backup_usb')
    if get_new_backup_ssd() == -1:
        return -1
    record_script_execution('get_new_backup_ssd')


if __name__ == '__main__':
    main()

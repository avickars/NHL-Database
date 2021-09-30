from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC

from DraftKings.contest_generator import get_contests
from DraftKings.contest_details_generator import get_contest_details
from DraftKings.contest_payout_summary_generator import get_payout_summary
from DraftKings.contest_game_types_generator import get_new_game_types
from DraftKings.contest_player_info_generator import get_player_info_api
from DraftKings.contest_player_info_webdriver_generator import get_player_info_webdriver
from DraftKings.draft_kings_script_execution import record_script_execution


def main():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # Getting Contests
    contests = get_contests(cursor)
    if contests == -1:
        conn.close()
        return -1
    connection.commit()
    record_script_execution('get_contests')

    # Getting contest details
    if get_contest_details(cursor, contests) == -1:
        conn.close()
        return -1
    connection.commit()
    record_script_execution('get_contest_details')

    # Getting the payout summary of the contest
    if get_payout_summary(cursor, contests) == -1:
        conn.close()
        return -1
    connection.commit()
    record_script_execution('get_payout_summary')

    # Getting the game type (contest rules) for each contest its not already there
    if get_new_game_types(cursor, connection) == -1:
        conn.close()
        return -1
    connection.commit()
    record_script_execution('get_new_game_types')

    # Getting the player info from the API
    if get_player_info_api(cursor, connection) == -1:
        conn.close()
        return -1
    connection.commit()
    record_script_execution('get_player_info_api')

    # Getting the player info from the webdriver
    if get_player_info_webdriver(cursor, connection) == -1:
        conn.close()
        return -1
    connection.commit()
    record_script_execution('get_player_info_webdriver')

    conn.close()


if __name__ == '__main__':
    main()

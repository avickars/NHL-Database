from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC

from DraftKings.contest_info_generator import get_contests_info
from DraftKings.contest_details_generator import get_contest_details
from DraftKings.contest_payout_summary_generator import get_payout_summary
from DraftKings.contest_game_types_generator import get_new_game_types
from DraftKings.contest_player_info_generator import get_player_info



def main():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # contests = get_contests_info(cursor)
    # if contests == -1:
    #     conn.close()
    #     return -1
    # connection.commit()
    #
    # if get_contest_details(cursor, contests) == -1:
    #     conn.close()
    #     return -1
    # connection.commit()
    #
    # if get_payout_summary(cursor, contests) == -1:
    #     conn.close()
    #     return -1
    # connection.commit()
    #
    # if get_new_game_types(cursor, connection) == -1:
    #     connection.commit()
    #     conn.close()
    #     return -1
    # connection.commit()
    if get_player_info(cursor, connection) == -1:
        conn.close()
        return -1
    connection.commit()

    conn.close()


if __name__ == '__main__':
    main()

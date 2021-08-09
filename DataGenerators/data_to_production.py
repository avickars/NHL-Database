from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC


def data_to_production():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    query = "call sp_conferences_view();"
    cursor.execute(query)
    connection.commit()

    query = "call sp_daily_update_script_execution_view();"
    cursor.execute(query)
    connection.commit()

    query = "call sp_divisions_view();"
    cursor.execute(query)
    connection.commit()

    query = "call sp_player_information_view();"
    cursor.execute(query)
    connection.commit()

    query = "call sp_skater_game_data_view();"
    cursor.execute(query)
    connection.commit()

    query = "call sp_schedules_view();"
    cursor.execute(query)
    connection.commit()

    query = "call sp_teams_view();"
    cursor.execute(query)
    connection.commit()

    query = "call sp_trophy_winners_view();"
    cursor.execute(query)
    connection.commit()

    query = "call sp_weekly_update_script_execution_view();"
    cursor.execute(query)
    connection.commit()

    conn.close()


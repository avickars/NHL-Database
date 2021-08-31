from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC


def data_to_production():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    # From Raw to Stage
    query = "call sp_game_prediction_team_stats_view();"
    cursor.execute(query)
    connection.commit()

    # # Stage to Stage
    # query = "call sp_average_gim_values_by_player_view();"
    # cursor.execute(query)
    # connection.commit()

    # query = "call sp_average_gim_values_by_season_position_view();"
    # cursor.execute(query)
    # connection.commit()

    # From Raw to Production
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


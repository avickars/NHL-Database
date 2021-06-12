from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC


def main():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    query = f"exec sp_conferences_view"
    cursor.execute(query)
    cursor.commit()
    query = f"exec sp_daily_update_script_execution"
    cursor.execute(query)
    cursor.commit()
    query = f"exec sp_divisions_view"
    cursor.execute(query)
    cursor.commit()
    query = f"exec sp_goalies_boxscores"
    cursor.execute(query)
    cursor.commit()
    query = f"exec sp_player_information"
    cursor.execute(query)
    cursor.commit()
    query = f"exec sp_skater_game_data"
    cursor.execute(query)
    cursor.commit()
    query = f"exec sp_sp_schedules"
    cursor.execute(query)
    cursor.commit()
    query = f"exec sp_teams_view"
    cursor.execute(query)
    cursor.commit()
    query = f"exec sp_trophy_winners_view"
    cursor.execute(query)
    cursor.commit()
    query = f"exec sp_yearly_update_script_execution"
    cursor.execute(query)
    cursor.commit()

    conn.close()



if __name__ == '__main__':
    main()
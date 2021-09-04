from DataGenerators.conference_generator import get_conferences
from DataGenerators.divisions_generator import get_divisions
from DataGenerators.franchise_generator import get_franchises
from DataGenerators.teams_generator import get_teams
from DataGenerators.seasons_generator import get_seasons
from DataGenerators.scipt_execution import record_script_execution
from DataGenerators.prospects_generator import get_prospects
from DataGenerators.drafts_generator import get_drafts, update_prospects
from DataGenerators.trophy_generator import get_trophies
from DataGenerators.trophy_winner_generator import get_trophy_winners
from ETL.etl_yearly_gim_consolidation import gim_yearly_update
from SQLCode import DatabaseConnection
from SQLCode import DatabaseCredentials as DBC
from DataGenerators.team_logo_generator import get_logos

def main():
    # Opening connection
    creds = DBC.DataBaseCredentials()
    conn = DatabaseConnection.sql_connection(creds.server, creds.database, creds.user, creds.password)
    connection = conn.open()
    cursor = connection.cursor()

    if gim_yearly_update() == -1:
        return -1
    record_script_execution('gim_yearly_update')

    if get_conferences() == -1:
        return -1
    record_script_execution('get_conferences')

    if get_divisions() == -1:
        return -1
    record_script_execution('get_divisions')

    if get_franchises() == -1:
        return -1
    record_script_execution('get_franchises')

    if get_teams() == -1:
        return -1
    record_script_execution('get_teams')

    if get_seasons() == -1:
        return -1
    record_script_execution('get_seasons')

    if get_drafts() == -1:
        return -1
    record_script_execution('get_drafts')

    if update_prospects() == -1:
        return -1
    record_script_execution('update_prospects')

    if get_trophies() == -1:
        return -1
    record_script_execution('get_trophies')

    if get_trophy_winners() == -1:
        return -1
    record_script_execution('get_trophy_winners')

    # query = "call sp_weekly_update_script_execution_view();"
    # cursor.execute(query)
    # connection.commit()
    # record_script_execution('sp_weekly_update_script_execution_view')

    if get_logos() == -1:
        return -1
    record_script_execution('get_logos')



    conn.close()








if __name__ == '__main__':
    main()

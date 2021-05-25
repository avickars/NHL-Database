from DataGenerators.conference_generator import get_conferences
from DataGenerators.divisions_generator import get_divisions
from DataGenerators.franchise_generator import get_franchises
from DataGenerators.teams_generator import get_teams
from DataGenerators.seasons_generator import get_seasons
from DataGenerators.scipt_execution import record_script_execution
from DataGenerators.prospects_generator import get_prospects
from DataGenerators.drafts_generator import get_drafts


def main():
    get_conferences()
    record_script_execution('get_conferences')
    get_divisions()
    record_script_execution('get_divisions')
    get_franchises()
    record_script_execution('get_franchises')
    get_teams()
    record_script_execution('get_teams')
    get_seasons()
    record_script_execution('get_seasons')
    get_prospects()
    record_script_execution('get_prospects')
    get_drafts()
    record_script_execution('get_drafts')

if __name__ == '__main__':
    main()
from DataGenerators.drafts_generator import get_drafts, update_prospects
from DataGenerators.scipt_execution import record_script_execution


def main():
    # get_drafts()
    # record_script_execution('get_drafts')
    update_prospects()
    record_script_execution('update_prospects')

if __name__ == '__main__':
    main()
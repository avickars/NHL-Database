from DataGenerators.prospects_generator import get_prospects
from DataGenerators.scipt_execution import record_script_execution


def main():
    get_prospects()
    record_script_execution('get_prospects')


if __name__ == '__main__':
    main()

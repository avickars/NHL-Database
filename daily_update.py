from DataGenerators.schedule_updator import get_daily_schedule
from DataGenerators.scipt_execution import record_script_execution
from DataGenerators.live_data_generator import get_live_date


def main():
    # get_daily_schedule()
    # record_script_execution('get_daily_schedule')
    get_live_date()


if __name__ == '__main__':
    main()

from DataGenerators.headshot_generator import get_headshots
from DataGenerators.scipt_execution import record_script_execution

def main():
    get_headshots()
    record_script_execution('get_headshots')



if __name__ == '__main__':
    main()

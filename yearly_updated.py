from DataGenerators.conference_generator import get_conferences
from DataGenerators.divisions_generator import get_divisions


def main():
    get_conferences()
    get_divisions()

if __name__ == '__main__':
    main()
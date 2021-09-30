from pytz import timezone
from dateutil import parser


def timezone_converter(datetime_obj):
    return datetime_obj.astimezone(timezone('US/Pacific'))


def main():
    datetime_obj = parser.parse('2021-09-29T23:00:00.0000000Z')
    date_format = '%Y-%M-%d %H:%M:%S'

    print('Current date & time is:', datetime_obj.strftime(date_format))

    print('Local date & time is  :', timezone_converter(datetime_obj).strftime(date_format))


if __name__ == '__main__':
    main()

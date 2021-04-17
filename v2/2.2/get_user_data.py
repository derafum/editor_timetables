from schedule import Schedule
from settings import *


def get_data():
    if DEBUG:
        with open('../../data/import_20_6.csv') as file:
            lines = file.read().splitlines()
            schedule = Schedule([list(map(int, line.split(';'))) for line in lines])
        name_to_save = 'debug_export'
    else:
        name_file = input('Введите имя импортируемого файла [.csv]: ')
        with open(name_file + '.csv') as file:
            lines = file.read().splitlines()
            shifts = [list(map(int, line.split(';'))) for line in lines]
            schedule = Schedule(shifts)
        name_to_save = input('Введите имя файла для сохранения результата [.csv]: ')

    return schedule, name_to_save


def save_to_csv(name, timetables):
    with open(name + '.csv', 'w') as file:
        for i, schedule in enumerate(timetables, 1):
            if len(timetables) > 1:
                file.write('Расписание № ' + str(i) + '\n')
            for shift in schedule:
                file.write(';'.join(map(str, shift)) + '\n')
            file.write('\n')

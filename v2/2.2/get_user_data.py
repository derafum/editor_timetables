from schedule import Schedule
from settings import *
import csv


def get_data():
    if DEBUG:
        people_in_total_and_in_shift = [20, 6]
        name_file = '../../data/import_20_6'
        with open(name_file + '.csv') as file:
            reader = csv.reader(file, delimiter=';', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            schedule = Schedule(people_in_total_and_in_shift, [list(map(int, row)) for row in reader])
        name_to_save = 'test'
    else:
        people_in_total_and_in_shift = list(map(int, [input('Введите количество человек: '),
                                                      input('Введите количество человек в смене: ')]))
        name_file = input('Введите имя импортируемого файла [.csv]: ')
        with open(name_file + '.csv') as file:
            reader = csv.reader(file, delimiter=';', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            schedule = Schedule(people_in_total_and_in_shift, [list(map(int, row)) for row in reader])
        name_to_save = input('Введите имя файла для сохранения результата [.csv]: ')

    return schedule, name_to_save + '_' + '_'.join(map(str, people_in_total_and_in_shift))


def save_to_csv(name, timetables):
    with open(name + '.csv', 'w', newline='') as isfile:
        writer = csv.writer(isfile, delimiter=";")
        for i, schedule in enumerate(timetables, 1):
            if len(timetables) > 1:
                writer.writerow(['Расписание № ' + str(i)])
            for shift in schedule:
                writer.writerow(shift)
            writer.writerow([''])

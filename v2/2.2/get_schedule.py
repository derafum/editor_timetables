from schedule import Schedule
import csv

debug = True


def get_schedule():
    if debug:
        people_in_total_and_in_shift = [10, 6]
        name_file = '../../data/import_10_6'
        with open(name_file + '.csv') as file:
            reader = csv.reader(file, delimiter=';', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            schedule = Schedule(people_in_total_and_in_shift, [list(map(int, row)) for row in reader])
        # schedule.read()
    else:
        people_in_total_and_in_shift = map(int, input('Введите количество человек: '),
                                           input('Введите количество человек в смене: '))
        name_file = input('Введите имя файла [имя по умолчанию: import]: ')
        name_file = '../../data/import_10_6' if name_file == '' else name_file
        with open(name_file + '.csv') as file:
            reader = csv.reader(file, delimiter=';', quotechar=',', quoting=csv.QUOTE_MINIMAL)
            schedule = Schedule(people_in_total_and_in_shift, [list(map(int, row)) for row in reader])

    return schedule

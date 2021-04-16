import os
import csv
from get_schedule import get_schedule


def save_to_csv(name, timetables):
    with open(name + '.csv', 'w', newline='') as isfile:
        writer = csv.writer(isfile, delimiter=";")
        for i, schedule in enumerate(timetables, 1):
            writer.writerow(['Расписание № ' + str(i)])
            for shift in schedule:
                writer.writerow(shift)
            writer.writerow([''])


name_file = 'temp.txt'


def save(mass):
    """Записывает результаты в файл"""
    with open(name_file, mode='a') as f:
        if len(mass) and mass not in load():
            f.write(str(mass) + '\n')


def load():
    """Загружает содержимое из файла"""
    with open(name_file, mode='r') as f:
        return [eval(elem) for elem in f.read().splitlines()]


def squeeze_the_schedule(schedule):
    """Ужимает, и сохраняет свой вариант"""
    while True:
        # Если все встретились
        if schedule.count_unmet == 0:
            # Сохраняем и сокращаем расписание
            schedule.save()
            # При возникновении нескольких смен под удаление рассматриваются все варианты
            for timetable in schedule.cut():
                squeeze_the_schedule(timetable)
        else:
            # Пробуем изменить расписание
            schedule.change()
            # Если не вышло завершаем работу функции
            if not schedule.changed:
                # Восстанавливаем последний рабочий вариант
                schedule.load()
                break
    save(schedule.shifts)


def main(schedule):
    """Основной алгоритм"""
    """Выбирает расписания с минимальным кол-вом смен"""
    squeeze_the_schedule(schedule)
    roll = load()
    min_count_shift = min([len(schedule) for schedule in roll])
    os.remove(name_file)
    save_to_csv(input('Введите имя файла для сохранения результата: '),
                [schedule for schedule in roll if len(schedule) == min_count_shift])


if __name__ == '__main__':
    main(get_schedule())

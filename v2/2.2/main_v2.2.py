from get_user_data import get_data, save_to_csv
from schedule import print_timetables
from settings import *
import os


def clear_temp():
    f = open(NAME_TEMP_FILE, 'w')
    f.close()


def save_to_temp(mass):
    """Записывает результаты в файл"""
    with open(NAME_TEMP_FILE, 'a') as f:
        if len(mass) and mass not in load_from_temp():
            f.write(str(mass) + '\n')


def load_from_temp():
    """Загружает содержимое из файла"""
    with open(NAME_TEMP_FILE) as f:
        return [eval(elem) for elem in f.read().splitlines()]


def squeeze_the_schedule(schedule, shrinkage_is_checked=False):
    """Ужимает, и сохраняет свой вариант"""
    there_is_a_working_option = False
    while True:
        # Если все встретились
        if schedule.count_unmet == 0:
            # Сохраняем и сокращаем расписание
            print('Все встретились')
            schedule.read()
            schedule.save()
            if shrinkage_is_checked:
                there_is_a_working_option = True
            # При возникновении нескольких смен под удаление рассматриваются все варианты
            if len(schedule.shortened_shifts) > 1:
                norm_view = list(map(lambda x: x + 1, schedule.shortened_shifts))
                print('Есть несколько вариантов удаления смен:', norm_view)
                managed_to_shrink = []
                for i, index in enumerate(schedule.shortened_shifts, 1):
                    print('Рассмотрим вариант с удалением', index + 1, 'смены:')
                    managed_to_shrink.append(squeeze_the_schedule(schedule.temp(index), True))
                    if i != len(schedule.shortened_shifts):
                        print('\nВозвращаемся к выбору', norm_view)
                        schedule.read()
                # Если не один из вариантов дальнейшего удаления смен не привёл к результату выводим последний рабочий
                if not any(managed_to_shrink):
                    print('Не один из вариантов удаления смен', norm_view, ' не приводит к результату')
                    print('Возвращаю последний рабочий вариант, запомню его:')
                    schedule.read()
                    schedule.load()
                    save_to_temp(schedule.shifts)
                # По завершению перебора вариантов выходим из цикла While
                break
            else:
                schedule.cut(schedule.shortened_shifts[0])
        else:
            # Пробуем изменить расписание
            schedule.change()
            # Если не вышло завершаем работу функции
            if not schedule.changed:
                # Восстанавливаем последний рабочий вариант
                schedule.load()
                if len(schedule.shifts):
                    print('Запомню тот вариант.')
                    save_to_temp(schedule.shifts)
                else:
                    print('Это тупиковый вариант...\n')
                break
    return there_is_a_working_option


def main():
    """Выбирает расписания с минимальным кол-вом смен"""
    schedule, name_to_save = get_data()

    clear_temp()
    print('Начинаю работу:')
    squeeze_the_schedule(schedule)
    print('Я закончил свою работу.')

    roll = load_from_temp()
    min_count_shift = min([len(schedule) for schedule in roll])
    os.remove(NAME_TEMP_FILE)
    timetables = [schedule for schedule in roll if len(schedule) == min_count_shift]

    print('Результат:')
    print_timetables(timetables)
    save_to_csv(name_to_save, timetables)
    if not DEBUG:
        input('Для выхода нажмите Enter')


if __name__ == '__main__':
    main()

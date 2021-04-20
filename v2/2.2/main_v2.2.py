from get_user_data import get_data, save_to_csv
from schedule import print_timetables
from settings import *


def record_schedule(schedule, results_timetables):
    if schedule not in results_timetables:
        if use_temp_file:
            with open(name_temp_file, mode='a') as f:
                f.write(str(schedule) + '\n')
        results_timetables.append(schedule)


def squeeze_the_schedule(schedule, results_timetables, shrinkage_is_checked=False):
    """Ужимает, и сохраняет свой вариант"""
    there_is_a_working_option = False
    while True:
        # Если все встретились
        if schedule.count_unmet == 0:
            # Сохраняем и сокращаем расписание
            if display_work and display_all_meet:
                print('Все встретились')
                schedule.read()
            schedule.save()
            if shrinkage_is_checked:
                there_is_a_working_option = True
            # При возникновении нескольких смен под удаление рассматриваются все варианты
            if len(schedule.shortened_shifts) > 1 and consider_all_deletion_options:
                norm_view = list(map(lambda x: x + 1, schedule.shortened_shifts))
                if display_work and display_variants_for_delete:
                    print('Есть несколько вариантов удаления смен:', norm_view)
                managed_to_shrink = []
                for i, index in enumerate(schedule.shortened_shifts, 1):
                    if display_work and display_consideration_of_disposal_options:
                        print('Рассмотрим вариант с удалением', index + 1, 'смены:')
                    managed_to_shrink.append(squeeze_the_schedule(schedule.temp(index), results_timetables, True))
                    if i != len(schedule.shortened_shifts):
                        if display_work and display_consideration_of_disposal_options:
                            print('\nВозвращаемся к выбору', norm_view)
                            schedule.read()
                # Если не один из вариантов дальнейшего удаления смен не привёл к результату выводим последний рабочий
                if not any(managed_to_shrink):
                    if display_work and display_consideration_of_disposal_options:
                        print('Не один из вариантов удаления смен', norm_view, ' не приводит к результату')
                        print('Возвращаю последний рабочий вариант, запомню его:')
                        schedule.read()
                    schedule.load()
                    record_schedule(schedule.shifts, results_timetables)
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
                    record_schedule(schedule.shifts, results_timetables)
                    if display_work and display_cant_change:
                        print('Запомню тот вариант.')
                else:
                    if display_work and display_cant_change:
                        print('Это тупиковый вариант...\n')
                    pass
                break
    return there_is_a_working_option


def main():
    """Выбирает расписания с минимальным кол-вом смен"""
    schedule, name_to_save = get_data()
    if view_temp_file:
        results_timetables = [eval(schedule) for schedule in open(input('name temp file: ')).read().splitlines()]
    else:
        results_timetables = []
        if use_temp_file:
            open(name_temp_file, mode='w').close()

        print('Начинаю работу...')
        squeeze_the_schedule(schedule, results_timetables)
        print('Я закончил свою работу.')

    min_count_shift = min([len(schedule) for schedule in results_timetables])
    timetables = [schedule for schedule in results_timetables if len(schedule) == min_count_shift]

    print('Результат:')
    print_timetables(timetables)
    save_to_csv(name_to_save, timetables)
    if not DEBUG:
        input('Для выхода нажмите Enter')


if __name__ == '__main__':
    main()

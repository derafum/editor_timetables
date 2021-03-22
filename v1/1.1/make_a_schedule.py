from itertools import combinations, chain
from collections import Counter


def generation_list(total_person):
    """Создает список человек"""
    return [x + 1 for x in range(total_person)]


def count_elements(general_list, list_of_elements):
    """Считает количество переданных элементов в списке"""
    count = Counter(general_list)
    res = {i: count[i] for i in list_of_elements}
    return res


def get_a_combination(roll, count=2, iterable=False):
    """Составляет все пары для списка
    (также можно использовать для генерации любых других
    сочетаний указывая второй параметр, а ещё получать итерируемый объект)"""
    if iterable:
        return combinations(roll, count)
    else:
        return list(combinations(roll, count))


def find_pairs(schedule):
    """Функция составляет пары для каждой смены в переданном расписании"""
    return [get_a_combination(shift) for shift in schedule]


def concatenate_lists(lists):
    """Функция сцепляет несколько списков в один"""
    return list(chain(*lists))


def did_everyone_meet(schedule, all_pairs):
    """Проверяет все ли встетились в переданном расписании"""
    return 0 not in count_elements(concatenate_lists(find_pairs(schedule)), all_pairs).values()


def calc(number_of_people, people_in_shift):
    """Считает расписания с указанными данными"""
    # Определение задачи
    list_people = generation_list(number_of_people)
    all_pairs = get_a_combination(list_people)
    all_shifts = get_a_combination(list_people, people_in_shift)
    list_schedule = []

    number_of_shifts = 0
    find_min_count_shift = True
    while find_min_count_shift:
        # Итерируемый объект - все варианты расписаний для переданного кол-ва смен
        timetables = get_a_combination(all_shifts, number_of_shifts, True)
        for schedule in timetables:
            if did_everyone_meet(schedule, all_pairs):
                find_min_count_shift = False
                list_schedule.append(schedule)
        number_of_shifts += 1
    return list_schedule


if __name__ == '__main__':
    i, j = map(int, input('Кол-во игроков и кол-во людей в смене (через пробел): ').split())
    timetables = calc(i, j)
    [print(i) for i in timetables]
    input()

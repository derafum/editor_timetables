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

def paring(roll, count_in_pair = 2):
    """Составляет все пары для списка
    (также можно использовать для генерации любых других
    сочетаний указывая второй параметр)"""
    return list(combinations(roll, count_in_pair))

def find_pairs(schedule):
    """Функция составляет пары для каждой смены в переданном расписании"""
    return [paring(shift) for shift in schedule]

def concatenate_lists(lists):
    """Функция сцкпляет несколько списков в один"""
    return list(chain(*lists))

if __name__ == '__main__':
    """Исключительно для теста модуля"""
    schedule = [
        (1, 2, 3, 6, 7, 8),
        (1, 2, 4, 5, 7, 9),
        (1, 3, 5, 6, 9, 10),
        (2, 4, 6, 7, 8, 10),
        (3, 4, 5, 6, 8, 9)]
    # Общее кол-во людей
    number_of_people = 10
    # Кол-во людей в смене
    people_in_shift = 6
    # Список ID охранников
    list_people = generation_list(number_of_people)
    # Все возможные смены
    all_shifts = paring(list_people, people_in_shift)
    # Все пары
    all_pairs = paring(list_people)
    # Пары для каждой смены
    couples_in_shifts = find_pairs(schedule)
    # Количество встреч каждой из пар в расписании
    number_of_meetings = count_elements(concatenate_lists(couples_in_shifts), all_pairs)

    print(
    f'number_of_people:{number_of_people}\n'
    f'people_in_shift:{people_in_shift}\n'
    f'list_people:{list_people}\n'
    f'schedule:{schedule}\n'
    # f'couples_in_shifts:{couples_in_shifts}\n'
    # f'all_shifts:{all_shifts}\n'
    # f'all_pairs:{all_pairs}\n'
    f'number_of_meetings:{number_of_meetings}\n'
    )

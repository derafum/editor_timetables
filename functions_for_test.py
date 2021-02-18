from itertools import combinations, chain
from collections import Counter
import csv


def generation_list(total_person):
    """Создает список человек"""
    return [x + 1 for x in range(total_person)]


def count_elements(general_list, list_of_elements):
    """Считает количество переданных элементов в списке"""
    count = Counter(general_list)
    res = {i: count[i] for i in list_of_elements}
    return res


def paring(roll, count_in_pair=2):
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


def find_unmet(schedule, all_pairs):
    """Возвращает пары которые не встретились"""
    # Кол-во встреч каждой из пар (словарь пара:кол-во)
    number_of_meetings = count_elements(list(chain(*find_pairs(schedule))), all_pairs)
    return [pair for pair, count in number_of_meetings.items() if count == 0]


def calc_count_unmet(schedule, all_pairs):
    """Считает количество невстретившихся пар в расписании"""
    return len(find_unmet(schedule, all_pairs))


def find_shifts_for_change(schedule, all_pairs):
    """Находит смены в которых находятся не встретившиеся люди"""
    people_unmet = set(concatenate_lists(find_unmet(schedule, all_pairs)))
    return list(set(i for i, shift in enumerate(schedule) for people in people_unmet if people in shift))


def change_shift(schedule, index, all_shifts, all_pairs):
    """Функция перебирает все смены для выбранной и выбирает ту в которой кол-во невстретившихся меньше"""
    test_schedule = schedule.copy()
    test_schedule.pop(index)
    for shift in all_shifts:
        new_schedule = test_schedule.copy()
        new_schedule.append(shift)
        if calc_count_unmet(new_schedule, all_pairs) < calc_count_unmet(schedule, all_pairs):
            return new_schedule
    return schedule


def calc_index_shifts(schedule, all_pairs):
    """Считает какие смены можно сократить"""
    # Пары для каждой смены образовавшиеся в нашем (переданном в функцию) расписании
    couples_in_shifts = find_pairs(schedule)
    # Кол-во встреч каждой из пар (словарь пара:кол-во)
    number_of_meetings = count_elements(list(chain(*couples_in_shifts)), all_pairs)
    # минимальное кол-во встреч
    minimum_number_of_meetings = min(list(filter(lambda x: x != 0, number_of_meetings.values())))
    # Список пар кол-во встреч которых минимально
    couples_with_min_number_meetings = [pair for pair, quantity in number_of_meetings.items() if
                                        quantity == minimum_number_of_meetings]
    # Количество пар встречавшихся наименьшее количество раз для каждой смены
    number_of_couples_with_min_meetings = [
        sum(count_elements(pair, couples_with_min_number_meetings).values()) for
        pair in couples_in_shifts]
    # Список номеров смен с наименьшим количеством пар встретившихся мин кол-во раз
    list_of_shift_numbers = [i for i, value in enumerate(number_of_couples_with_min_meetings) if
                             value == min(number_of_couples_with_min_meetings)]
    return list_of_shift_numbers


def get_information_from_the_user():
    # ======================Получение необходимой информации от пользователя=================
    err = True
    while err:
        number_of_people = input('Введите количество человек: ')
        people_in_shift = input('Введите количество человек в смене: ')
        if number_of_people.isdigit() and people_in_shift.isdigit():
            number_of_people = int(number_of_people)
            people_in_shift = int(people_in_shift)
            if (number_of_people > 0) and (people_in_shift > 1) and (number_of_people >= people_in_shift):
                list_people = generation_list(number_of_people)  # Список людей
                err = False
        import_shifts = []
        if input('Хотите ли вы импортировать данные [y/n]: ').lower() == 'y':
            with open('import.csv') as File:
                reader = csv.reader(File, delimiter=';', quotechar=',', quoting=csv.QUOTE_MINIMAL)
                for row in reader:
                    import_shifts.append(row)
                # Проверка каждой ячейки (каждая ячейка должна быть целым числом - номером охранника)
                check_import_data = True
                for j in import_shifts:
                    for i in j:
                        if not (i.isdigit()):
                            check_import_data = False
                if check_import_data and not (err):
                    import_shifts = [[int(i) for i in j] for j in import_shifts]
                    # Проверка на то что среди импортированных не окажется посторонний
                    import_humans = set(concatenate_lists(import_shifts))
                    for human in import_humans:
                        if human not in list_people:
                            err = True
                    # Проверка на количество людей в каждой импортированной смене (колжно соответствовать указанному выше)
                    for smena in import_shifts:
                        if len(smena) != people_in_shift:
                            err = True
                else:
                    err = True
        if err:
            print('Проверьте корректность введённых данных.')
    ask_before_recording = False
    if input('Спрашивать перед каждой записью найденных расписаний [y/n]: ').lower() == 'y':
        ask_before_recording = True
    return number_of_people, people_in_shift, import_shifts, ask_before_recording, list_people


if __name__ == '__main__':
    """Исключительно для теста модуля"""
    schedule = [
        (1, 2, 3, 6, 7, 8),
        (1, 2, 4, 5, 7, 9),
        (1, 3, 5, 6, 9, 10),
        (2, 4, 6, 7, 8, 10),
        (3, 4, 5, 6, 8, 9)
    ]
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
    # Кол-во невстретившихся пар
    count_unmet = calc_count_unmet(schedule, all_pairs)

    print(
        f'number_of_people:{number_of_people}\n'
        f'people_in_shift:{people_in_shift}\n'
        f'list_people:{list_people}\n'
        f'schedule:{schedule}\n'
        # f'couples_in_shifts:{couples_in_shifts}\n'
        # f'all_shifts:{all_shifts}\n'
        # f'all_pairs:{all_pairs}\n'
        f'number_of_meetings:{number_of_meetings}\n'
        f'count_unmet:{count_unmet}\n'
        # f'{find_unmet(schedule, all_pairs)}\n'
        # f'{find_shifts_for_change(schedule, all_pairs)}\n'
        f'{calc_index_shifts(schedule, all_pairs)}'
    )

import itertools
import csv


# Формурует все возможные комбинации
def formation_of_combinations(bill, quantity):
    return itertools.combinations(bill, quantity)


# print([x for x in formation_of_combinations((1,2,3,4),3)])

# Создает список человек
def generation_list(total_person):
    return [x + 1 for x in range(total_person)]


# Создает список со встречами для каждого расписания [(1,2,3),(2,3,1)...]
def generation_of_schedule_pairs(required_schedules, all_pairs):
    return [(count_pairs(concatenate_lists(find_pairs(timetable)), all_pairs)) for timetable in required_schedules]


# Генерирует все возможные пары элементов из списка
def pairing(list_people):
    couples = []
    for i in range(len(list_people)):
        for j in range(i + 1, len(list_people)):
            couples.append((list_people[i], list_people[j]))
    return couples


# print(pairing((1,2,3,4,5)))

# Находит пары для каждой смены в переданном расписании
def find_pairs(schedule):
    pairs = []
    for pair in schedule:
        pairs.append(pairing(pair))
    return pairs


# print(find_pairs([(1,2,3),(2,3,4)]))

# Получает список из списков и обьединяет их содержимое в один
def concatenate_lists(lists):
    linked = []
    for i in range(len(lists)):
        for j in range(len(lists[i])):
            linked.append(lists[i][j])
    return linked


# print(concatenate_lists([((1,2),(2,3)),((1,3),(3,4))]))

# Считает количество пар в списке
def count_pairs(list_of_pairs, pairs):
    summ = []
    for i in range(len(pairs)):
        summ.append(list_of_pairs.count(pairs[i]))
        # print(pairs[i], list_of_pairs.count(pairs[i]))
    return summ


# print(count_pairs([(1,2),(1,3),(1,2)],[(0,1),(1,2)]))

# Функция находит решение путем перебора сочетаний, плохо работает вовсе для больших чисел
def search_for_compositions(all_shifts, all_pairs, import_shifts, number_of_people, people_in_shift,
                            ask_before_recording):
    # Пробуем составить расписания увеличивая количество смен до тех пор пока не найдется расписанию удовлетворяющее условию: каждый пересёкся с каждым хотябы раз.
    number_of_shifts = 0
    data = {
        'all_pairs': all_pairs,
        'number_of_people': number_of_people,
        'people_in_shift': people_in_shift,
        'schedule': [],
        'number_of_pairs': []
    }
    run = True
    while run:
        # print(all_shifts, number_of_shifts)
        # Все возможные расписания для количества смен
        timetables = formation_of_combinations(all_shifts, number_of_shifts)
        # print(timetables)
        for schedule in timetables:
            # Добавление импортированных смен если таковые имеются
            schedule = concatenate_lists([schedule, import_shifts])
            # Составление списка пар для каждой смены данного расписания
            pairs = find_pairs(schedule)
            # Объединение всех пар в один список
            general_list_with_all_pairs = concatenate_lists(pairs)
            # Подсчёт количества пар в списке
            number_of_pairs = count_pairs(general_list_with_all_pairs, all_pairs)
            # Проверяем есть ли в нашем расписании не встретившиеся
            if 0 not in number_of_pairs:
                run = False
                # Если в расписании каждый с каждым встретился сохраняем это расписание и прекращаем увеличение количества смен
                for smena in schedule:
                    print(smena)
                print()
                if ask_before_recording:
                    if input('Записать этот вариант [y/n]: ').lower() == 'y':
                        data['schedule'].append(schedule)
                        data['number_of_pairs'].append(number_of_pairs)
                    if input('Искать дальше [y/n]: ').lower() == 'n':
                        break
                else:
                    data['schedule'].append(schedule)
                    data['number_of_pairs'].append(number_of_pairs)
        number_of_shifts += 1
    print('Поиск завершён.')
    return data


# Функция сохраняет данные в csv
def save_to_csv(data):
    with open('export.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=";")
        for i in range(len(data['schedule'])):
            writer.writerow(['Расписание № ' + str(i + 1)])
            for smena in data['schedule'][i]:
                writer.writerow(smena)
            writer.writerow([''])


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
            with open('../data/import_20_6.csv') as File:
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


def main():
    number_of_people, people_in_shift, import_shifts, ask_before_recording, list_people = get_information_from_the_user()  # Получение необходимой информации от пользователя
    all_shifts = list(formation_of_combinations(list_people, people_in_shift))  # Все возможные смены
    all_pairs = pairing(list_people)  # Все возможные пары
    data = search_for_compositions(all_shifts, all_pairs, import_shifts, number_of_people, people_in_shift,
                                   ask_before_recording)  # Список расписаний
    if len(data['schedule']) > 0:
        save_to_csv(data)
    input()


if __name__ == '__main__':
    main()

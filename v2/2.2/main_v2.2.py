from get_schedule import get_schedule


def main(schedule):
    """Основной алгоритм"""
    while True:
        # Если все встретились
        if schedule.count_unmet == 0:
            # Сохраняем и сокращаем расписание
            print('все встретились')
            # schedule.read()
            schedule.save()
            schedule.cut()
        else:
            # Пробуем изменить расписание
            schedule.change()
            # Если не вышло завершаем работу программы
            if not schedule.changed:
                # Восстанавливаем последний рабочий вариант
                schedule.load()
                break
    print()
    print('Результат:')
    schedule.read()
    return schedule.shifts


if __name__ == '__main__':
    main(get_schedule())

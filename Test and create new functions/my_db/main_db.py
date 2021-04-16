name = 'test_db.txt'


def save(mass):
    with open(name, mode='a') as f:
        f.write(str(mass) + '\n')


def load():
    with open(name, mode='r') as f:
        return [eval(elem) for elem in f.read().splitlines()]

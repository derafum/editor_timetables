import os

name = 'test_db.txt'


def save(mass):
    with open(name, 'a') as f:
        f.write(str(mass) + '\n')


def load():
    with open(name) as f:
        return [eval(elem) for elem in f.read().splitlines()]


[save(list(range(1, 10 + 1))) for i in range(5)]
print(load())
os.remove(name)
input()

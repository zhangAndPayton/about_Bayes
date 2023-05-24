import random
import matplotlib.pyplot as plt


LOW = 1
HIGH = 4
MODE = [2, 2, 2]

NUMS = 10000


def getOneTrianguler(low, high, mode):

    return round(random.triangular(low, high, mode))


def myCount(result):

    newResult = {}

    for r in result:
        if r in newResult.keys():
            newResult[r] += 1
        else:
            newResult[r] = 1

    newResult = dict(sorted(newResult.items(), key=lambda x: x[0]))

    return list(newResult.keys()), list(newResult.values())


result = [[],[],[]]
for i in range(NUMS):
    result[0].append(getOneTrianguler(LOW, HIGH, MODE[0]))
    result[1].append(getOneTrianguler(LOW, HIGH, MODE[1]))
    result[2].append(getOneTrianguler(LOW, HIGH, MODE[2]))


plt.plot(*myCount(result[0]), label=f"mode={MODE[0]}")
plt.plot(*myCount(result[1]), label=f"mode={MODE[1]}")
plt.plot(*myCount(result[2]), label=f"mode={MODE[2]}")

plt.legend()
plt.show()


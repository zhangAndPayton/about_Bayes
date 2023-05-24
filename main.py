import sys
from search import Search

def printMenu():

    result = []

    result.append(input("是否放弃搜索: "))
    if result[0] == "是":
        print("已放弃搜索。")
        sys.exit(0)

    result.append(eval(input("第一支搜索队派往区域: ")))
    result.append(eval(input("第二支搜索队派往区域: ")))

    return result

def printPAndE(P, E):

    for i in range(len(P)):
        print(f"p{i+1}={P[i]:.2f}", end="  ")

    print()

    for i in range(len(E)):
        print(f"e{i+1}={E[i]:.2f}", end="  ")

    print()

def main():

    task = Search()
    task.getSailorPosition()

    day = 0
    lastRegion = [0, 0]

    while True:

        day += 1


        task.SEPWithWeather()
        printPAndE(task.p, task.e)
        task.getMap(lastRegion)

        result = printMenu()

        regionOne = result[1]
        regionTwo = result[2]

        lastRegion = [regionOne, regionTwo]

        searchRegionOne = task.search(regionOne)
        searchRegionTwo = task.search(regionTwo)

        if regionOne == regionTwo:
            for j in range(len(task.e)):
                if j == (regionOne - 1):
                    task.e[j] = (len(set(searchRegionOne + searchRegionTwo))) / \
                                ((task.searchRegion[0].shape[0] * task.searchRegion[0].shape[1])**2)
                else:
                    task.e[j] = 0
        else:
            for j in range(len(task.e)):
                if j == (regionOne - 1):
                    pass
                elif j == (regionTwo - 1):
                    pass
                else:
                    task.e[j] = 0

        if task.flag == True:
            print(f"耗时{day}天成功找到目标，其坐标位于: {task.sailor}.")
            task.getMap([searchRegionOne, searchRegionTwo])
            sys.exit()
        else:
            task.getNewP()
            print(f"在第{day}天时未能成功找到目标.")

if __name__ == "__main__":
    main()

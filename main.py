import sys
from search import Search

def printMenu():

    # 打印菜单供用户交互使用，并收集用户在该次交互中的指令;
    result = []

    result.append(input("是否放弃搜索: "))
    if result[0] == "是":
        print("已放弃搜索。")
        sys.exit(0)

    result.append(eval(input("第一支搜索队派往区域: ")))
    result.append(eval(input("第二支搜索队派往区域: ")))

    return result

def printPAndE(P, E):

    # 格式化打印;
    for i in range(len(P)):
        print(f"p{i+1}={P[i]:.2f}", end="  ")

    print()

    for i in range(len(E)):
        print(f"e{i+1}={E[i]:.2f}", end="  ")

    print()

def main():

    task = Search()

    # 初始化船员位置;
    task.getSailorPosition()

    day = 0
    lastRegion = [0, 0]

    while True:

        day += 1

        # 生成当天各个搜索区域预期的搜索有效性，格式化打印概率与SEP信息;
        task.SEPWithWeather()
        printPAndE(task.p, task.e)

        # 显示地图，地图中给出了当天各个区域的天气情况以及上一次搜索的区域（绿色标注）;
        task.getMap(lastRegion)

        # 开始当天的搜索决策;
        result = printMenu()

        regionOne = result[1]
        regionTwo = result[2]

        # 记录当天的搜索决策，用于下一次搜索时地图上的区域标注;
        lastRegion = [regionOne, regionTwo]

        # 执行搜索（这里会产生搜索结果，记录在Search.flag中）;
        searchRegionOne = task.search(regionOne)
        searchRegionTwo = task.search(regionTwo)

        # 先更新当天进行的两次搜索的实际SEP结果;
        if regionOne == regionTwo:
            for j in range(len(task.e)):
                if j == (regionOne - 1):
                    # 两次搜索在同一位置进行，需要计算新的SEP（参考README.md）;
                    task.e[j] = (len(set(searchRegionOne + searchRegionTwo))) / \
                                ((task.searchRegion[0].shape[0] * task.searchRegion[0].shape[1])**2)
                else:
                    # 将其余区域的SEP还原为0;
                    task.e[j] = 0
        else:
            for j in range(len(task.e)):
                if j == (regionOne - 1):
                    pass
                elif j == (regionTwo - 1):
                    pass
                else:
                    # 将其余区域的SEP还原为0;
                    task.e[j] = 0

        if task.flag == True:
            print(f"耗时{day}天成功找到目标，其坐标位于: {task.sailor}.")
            # 找到之后更新一下地图;
            task.getMap(lastRegion)
            sys.exit()
        else:
            # 根据实际搜索的SEP重新计算下一次搜索的概率并更新在Search类中;
            task.getNewP()
            print(f"在第{day}天时未能成功找到目标.")

if __name__ == "__main__":
    main()

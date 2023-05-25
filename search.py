import sys
import random
import itertools
import numpy as np
import cv2

PATH_OF_MAP = r"cape_python.png"

# 用列表组织了搜索区域定义与每个区域对应的概率;
# 每个搜索区域的面积需要保证相同，且不能有重叠;
# 想要新增搜索区域，只需改动此处的代码即可;
# 搜索区域的定义方式是两个角点坐标，后面将其用于Array时需要注意坐标变换;
SEARCH_REGION = ((130, 265, 180, 315), (80, 255, 130, 305), (105, 205, 155, 255), (55, 195, 105, 245))
P = [0.2, 0.4, 0.3, 0.1]

# 两种天气，用于简易的天气系统以产生更灵活的搜索有效性SEP;
CLEAR_DAY = "c"
RAINY_DAY = "r"

class Search():

    def __init__(self):

        self.map = cv2.imread(PATH_OF_MAP, cv2.IMREAD_COLOR)
        if self.map is None:
            print(f"无法找到海域地图文件: {PATH_OF_MAP}.", file=sys.stderr)
            sys.exit(1)

        self.searchRegion = []
        for i in range(len(SEARCH_REGION)):
            self.searchRegion.append(self.map[SEARCH_REGION[i][1]: SEARCH_REGION[i][3],
                                     SEARCH_REGION[i][0]: SEARCH_REGION[i][2]])

        self.p = P

        self.e = [0 for _ in range(len(self.p))]

        # 存储了整幅地图中的船员位置;
        self.sailor = [0, 0]

        # 存储了在区域坐标下的船员位置;
        self.sailorInRegion = [0, 0]


        self.regionOfSailor = 0

        # 初始化天气系统，开始时均为雨天;
        self.weather = [RAINY_DAY for _ in range(len(self.e))]

        # 用于判断是否找到船员的关键flag变量;
        self.flag = False

    def getMap(self, lastSearch=[0, 0]):

        font = cv2.FONT_HERSHEY_PLAIN
        black = (0, 0, 0)
        green = (100, 180, 10)
        red = (10, 10, 250)
        lineWidth = 1

        # 绘制一个比例尺;
        cv2.line(self.map, (20, 370), (70, 370), black, lineWidth+1)
        cv2.putText(self.map, "0", (8, 370), font, lineWidth, black)
        cv2.putText(self.map, "50 Nautical Miles", (72, 370), font, lineWidth, black)

        # 用绿色填充上一次搜索中搜索过的区域;
        for i in range(0, len(SEARCH_REGION)):
            if i + 1 in lastSearch:
                cv2.rectangle(self.map, (SEARCH_REGION[i][0], SEARCH_REGION[i][1]),
                              (SEARCH_REGION[i][2], SEARCH_REGION[i][3]), green, -lineWidth)

        # 用红色填充上一次搜索中未搜索的区域;
        for i in range(0, len(SEARCH_REGION)):
            if i + 1 not in lastSearch:
                cv2.rectangle(self.map, (SEARCH_REGION[i][0], SEARCH_REGION[i][1]),
                              (SEARCH_REGION[i][2], SEARCH_REGION[i][3]), red, -lineWidth)

        # 为每个搜索区域增加黑色边框以及编号;
        for i in range(0, len(SEARCH_REGION)):
            cv2.rectangle(self.map, (SEARCH_REGION[i][0], SEARCH_REGION[i][1]),
                          (SEARCH_REGION[i][2], SEARCH_REGION[i][3]), black, lineWidth)
            cv2.putText(self.map, str(i+1) + "-" + f"{self.weather[i]}", (SEARCH_REGION[i][0] + 3, SEARCH_REGION[i][1] + 15),
                        font, lineWidth, black)

        # 若已经找到目标，则利用全局坐标标出目标位置;
        if self.flag == True:
            #cv2.putText(self.map, "*", (self.sailor[0], self.sailor[1]), font, lineWidth, red)
            cv2.drawMarker(self.map, (self.sailor[0], self.sailor[1]), red, markerType=0)
        cv2.imshow("Search Map", self.map)
        cv2.waitKey()

    def getSailorPosition(self):

        # 随机生成船员的区域坐标;
        xInRegion = np.random.choice(self.searchRegion[0].shape[1], 1)
        yInRegion = np.random.choice(self.searchRegion[0].shape[0], 1)

        self.sailorInRegion = [xInRegion, yInRegion]

        region = round(random.triangular(1, 4, 2))

        # 利用区域坐标三角分布生成的随机区域产生全局坐标;
        for i in range(0, len(SEARCH_REGION)):
            if (i + 1) == region:
                x = xInRegion + SEARCH_REGION[i][0]
                y = yInRegion + SEARCH_REGION[i][1]

        self.regionOfSailor = region

        # 全局坐标的计算中有Array类型变量参与，因此需要将坐标还原为int类型;
        self.sailor = [int(x), int(y)]

    def SEPWithWeather(self):
        # 需要注意的是，这里在SEP的生成中没有考虑是否进行了实际搜索;
        # 在后面实际指定了搜索区域时，没有进行搜索的区域的SEP需要被还原为0;

        for i in range(len(self.weather)):
            if self.weather[i] == CLEAR_DAY:
                # 如果前一天是晴天的话，生成较大的SEP;
                self.e[i] = random.triangular(0.5, 0.9)
                if self.e[i] < 0.55:
                    # 如果前一天是晴天的话，下一天是雨天的概率较小;
                    self.weather[i] = RAINY_DAY
            else:
                self.e[i] = random.triangular(0.1, 0.5)
                if self.e[i] > 0.3:
                    # 如果前一天是雨天的话，下一天是雨天的概率要稍微大一些;
                    self.weather[i] = CLEAR_DAY

    def search(self, region):

        xInRegion = range(self.searchRegion[0].shape[1])
        yInRegion = range(self.searchRegion[0].shape[0])

        # 生成用于遍历的整个区域网格坐标;
        xAndy = list(itertools.product(xInRegion, yInRegion))

        random.shuffle(xAndy)

        # 将随机打乱后的区域网格坐标截取，模拟出搜索有效性影响下的搜索;
        xAndyWithSEP = xAndy[: int(self.e[region - 1] * len(xAndy))]
        sailorInRegion = (self.sailorInRegion[0], self.sailorInRegion[1])

        # 搜索过程中没有使用全局坐标，这样大大简化了搜索逻辑;
        if region == self.regionOfSailor and sailorInRegion in xAndyWithSEP:
            self.flag = True

        # 需要将截取后的网格坐标返回，用于计算两次搜索同一个区域时新的SEP;
        return xAndyWithSEP

    def getNewP(self):

        # 这一部分的内容可以参考README.md中的介绍;
        denom = 0
        for i in range(len(self.p)):
            denom += self.p[i] * (1 - self.e[i])

        for i in range(len(self.p)):
            self.p[i] = self.p[i] * (1 - self.e[i]) / denom

if __name__ == "__main__":
    task = Search()








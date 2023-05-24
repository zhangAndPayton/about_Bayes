import sys
import random
import itertools
import numpy as np
import cv2

PATH_OF_MAP = r"cape_python.png"

SEARCH_REGION = ((130, 265, 180, 315), (80, 255, 130, 305), (105, 205, 155, 255), (55, 195, 105, 245))


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

        self.p = [0.2, 0.5, 0.3]

        self.e = [0, 0, 0]

        # 坐标的存储需要使用可变数据类型。
        self.sailor = [0, 0]
        self.regionOfSailor = 0

    def getMap(self, lastSearch=[0, 0]):

        font = cv2.FONT_HERSHEY_PLAIN
        black = (0, 0, 0)
        green = (100, 180, 10)
        red = (10, 10, 250)
        lineWidth = 1

        cv2.line(self.map, (20, 370), (70, 370), black, lineWidth+1)
        cv2.putText(self.map, "0", (8, 370), font, lineWidth, black)
        cv2.putText(self.map, "50 Nautical Miles", (72, 370), font, lineWidth, black)

        for i in range(0, len(SEARCH_REGION)):
            if i + 1 in lastSearch:
                cv2.rectangle(self.map, (SEARCH_REGION[i][0], SEARCH_REGION[i][1]),
                              (SEARCH_REGION[i][2], SEARCH_REGION[i][3]), green, -lineWidth)

        for i in range(0, len(SEARCH_REGION)):
            if i + 1 not in lastSearch:
                cv2.rectangle(self.map, (SEARCH_REGION[i][0], SEARCH_REGION[i][1]),
                              (SEARCH_REGION[i][2], SEARCH_REGION[i][3]), red, -lineWidth)

        for i in range(0, len(SEARCH_REGION)):
            cv2.rectangle(self.map, (SEARCH_REGION[i][0], SEARCH_REGION[i][1]),
                          (SEARCH_REGION[i][2], SEARCH_REGION[i][3]), black, lineWidth)
            cv2.putText(self.map, str(i+1), (SEARCH_REGION[i][0] + 3, SEARCH_REGION[i][1] + 15),
                        font, lineWidth, black)

        cv2.imshow("Search Map", self.map)
        cv2.waitKey()


if __name__ == "__main__":
    task = Search()
    task.getMap([2, 4])

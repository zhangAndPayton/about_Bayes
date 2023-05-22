import sys
import random
import itertools
import numpy as np
import cv2 as cv


MAP_FILE_PATH = 'cape_python.png'

# SEARCH_REGION_NUM = (UL-X, UL-Y, LR-X, LR-Y)
SEARCH_REGION_1 = (130, 265, 180, 315)
SEARCH_REGION_2 = (80, 255, 130, 305)
SEARCH_REGION_3 = (105, 205, 155, 255)


class Search():
    """Bayesian Search & Rescue game with three search areas."""


    def __init__(self):
        pass


    def drawMap(self):
        """Display basemap with scale, last know position (x, y) and search region."""

        pass


    def  generateActualLocation(self):
        """Return the actual (x, y) location of the missing sailor;"""

        pass


    def getSEP(self):
        """Get independent SEP of three search region."""

        pass


    def search(self):
        """Just search."""

        pass


if __name__ == '__main__':
    pass

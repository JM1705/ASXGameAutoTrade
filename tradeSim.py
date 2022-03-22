import random
import numpy as np
from matplotlib import pyplot as plt
priceList = []
cycleList = []
stockPrice = 50
cycle = 0
bounds = [0, 100]
while True:
    change = random.randint(-10, 10)
    priceAfterChange = stockPrice + change
    stockPrice += change * (1-((priceAfterChange-50)**8)/(50**8))
    priceList.append(stockPrice)
    cycleList.append(cycle)
    xp = np.array(cycleList)
    yp = np.array(priceList)
    plt.plot(xp, yp)
    plt.show()
    cycle += 1
    if len(cycleList) > 100:
        cycleList.pop(0)
        priceList.pop(0)
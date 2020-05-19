import csv
import numpy as np
import matplotlib.pyplot as plt


#first, finish up so that I can get the data i need and make one graph (nothing fancy, just a line graph)
#second, make a function that can get the data and make the visualization (will have lots of parameters)

#Initial preprocessing of SPX CSV, compiling lists of premium prices and dates for

class Option():
    def __init__(self, name, file):
        self.name = name
        self.file = file


    def createSPX2000StockVisual(self, file):
        with open(file, 'r') as csv_file:
            lines = csv_file.readlines()
            entireList = []
            stockNames = []
            dates_2300_call = []
            strike_2300_call_bid_prices = []
            for line in lines:
                lineList = line.split(',')
                stockNames.append(lineList[0])
                if lineList[4] == 'call' and line != lines[0] and lineList[7] == '2300':
                    strike_2300_call_bid_prices.append(lineList[12])
                for x in lineList:
                    if (x != '/n'):
                        entireList.append(x)

        print(len(stockNames))


def main():
    SPXOption = Option("SPX", 'SPX_20180904_to_20180928.csv')
    SPXOption.createSPX2000StockVisual('SPX_20180904_to_20180928.csv')

main()

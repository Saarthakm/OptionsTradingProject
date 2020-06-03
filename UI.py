import kivy
import numpy as np
import matplotlib.pyplot as plt
from dataCollector import Option
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.base import runTouchApp
from kivy.core.image import Image as CoreImage
from premiums_scraper import *




class OptionizeGrid(GridLayout):
    def __init__(self, **kwargs):
        super(OptionizeGrid, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Label(text="Optionize"))
        self.view_SPX = Button(text="View Static Option Premium Trends Plots")
        self.add_widget(self.view_SPX)
        self.view_SPX.bind(on_press = self.premiumPressed)
        self.view_SP500Dynamic = Button(text="View Live-Time SP500 Option Premium Trend Plots")
        self.add_widget(self.view_SP500Dynamic)
        self.ticker_search = TextInput(text='Enter a stock ticker here: ', multiline=False)
        self.add_widget(self.ticker_search)
        self.ticker_search.bind(on_text_validate=self.on_enter)




    def premiumPressed(self, instance):
        SPXOption = Option("SPX", 'SPX_20180904_to_20180928.csv')
        SPXOption.createSPX2000StockVisual('SPX_20180904_to_20180928.csv')
        data = {'a': np.arange(50),
                'c': np.random.randint(0, 50, 50),
                'd': np.random.randn(50)}
        data['b'] = data['a'] + 10 * np.random.randn(50)
        data['d'] = np.abs(data['d']) * 100

        plt.scatter('a', 'b', c='c', s='d', data=data)
        plt.xlabel('entry a')
        plt.ylabel('entry b')
        plt.show()

    def on_enter(self, instance):
        ticker = self.ticker_search.text
        self.ticker_search.text = "Enter a stock ticker here: "

        for x in self.ticker_search.text:
            if x

        for tickerNames in all_major_stocks_tickers:
            if ticker != tickerNames:
                print("This stock is not in S&P500, NASDAQ, or DOW! Please enter another valid ticker!")

        print(ticker)




class OptionizeUI(App):
    def build(self):
        return OptionizeGrid()




if __name__ == "__main__":
    OptionizeUI().run()

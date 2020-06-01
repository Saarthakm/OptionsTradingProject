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
        self.logo = CoreImage("OptionizeLogo.png")
        self.add_widget(self.logo)



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



class OptionizeUI(App):
    def build(self):
        return OptionizeGrid()




if __name__ == "__main__":
    OptionizeUI().run()

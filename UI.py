import kivy
import numpy as np
import matplotlib.pyplot as plt
from dataCollector import Option
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button




class OptionizeGrid(GridLayout):
    def __init__(self, **kwargs):
        super(OptionizeGrid, self).__init__(**kwargs)

        self.insideGrid = GridLayout()
        self.insideGrid.cols = 2
        self.insideGrid.add_widget(Label(text="SPY Premium Trends"))
        self.insideGrid.add_widget(TextInput(multiline=False))
        self.add_widget(self.insideGrid)
        self.cols = 2
        self.view_SPX = Button(text="SPX Premium Trends")
        self.add_widget(self.view_SPX)
        self.view_SPX.bind(on_press = self.premiumPressed)

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

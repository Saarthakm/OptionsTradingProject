import kivy
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
        self.view_SPX.bind(on_press = self.pressed)

    def premiumPressed(self, instance):
        



class OptionizeUI(App):
    def build(self):
        return OptionizeGrid()




if __name__ == "__main__":
    OptionizeUI().run()

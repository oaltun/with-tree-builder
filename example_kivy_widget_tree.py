from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from withtreebuilder import KivyTreeBuilder


class Layout1(BoxLayout):
    def __init__(self, **kwargs):
        super(Layout1, self).__init__(**kwargs)

        self.orientation = 'horizontal'

        node = KivyTreeBuilder()
        with node(self):
            with node(Button(text='btn1')): pass
            with node(Button(text='btn2')) as b: self.button = b

        print(self.button.text)
        print(self.children)


class Layout2(BoxLayout):
    def __init__(self, **kwargs):
        super(Layout2, self).__init__(**kwargs)

        node = KivyTreeBuilder()
        with node(self):
            with node(BoxLayout(orientation='vertical')):
                with node(Button(text='btn3')) as w: self.button = w
                with node(Label(text='lbl1')) as w: self.label = w
                with node(Layout1()): pass


class MyApp(App):
    def build(self):
        return Layout2()


if __name__ == '__main__':
    MyApp().run()

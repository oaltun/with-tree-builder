# with-tree-builder
This small library demonstrates how trees can be built using Python's with keyword.

## Idea

Compare this:
```python
node('root',
    [node('child0'),
     node('child1'),
     node('child2',[
        node('grand child')]])
```   
 With this:
 ```python
 with node('root'):
    with node('child0') as c: self.child0 = c  # Allows getting references to wanted nodes.
    with node('child1'): pass
    with node('child2'):
        # Any python code...
        with node('grand child'): pass
 ```   
 Much easier to write. Arguably easier to read. You can establish the parent-child relationships naturally, just like Python code. Allows getting references to tree nodes. Allows arbitrary Python code to be written between node additions. All Python: syntax checking, editor support, etc. are all already there.
 
 I got the idea of using `with` for this purpose while reading the [Paint Tutorial](https://kivy.org/docs/tutorials/firstwidget.html) of [Kivy](kivy.org) (search `with self.canvas:`). I checked their source code to see how they did it, and extracted related code into this class.
 
## Usage
 
Following is a full example of building a generic tree using with-tree-builder. 
```python
from withtreebuilder import WithTreeBuilder


class Node(object):
    def __init__(self, data=None):
        super(Node, self).__init__()
        self.data = data
        self.children = list()


class MyTree(Node):
    def __init__(self, data):
        super(MyTree, self).__init__(data)

        add = WithTreeBuilder()

        with add(self):
            with add(Node('child0')) as c: self.child0 = c
            with add(Node('child1')): pass
            with add(Node('child2')):
                with add(Node('child3')): pass

        print(self.child0.data)


my_tree = MyTree('root')

print (my_tree.children[2].children[0].data)

```

And following is a full simple [Kivy](http://kivy.org) application. In this example we need to overwrite the `add_child()` method, as using the `children` field of Kivy widgets directly is probably not a good idea. Instead we use the `Widget.add_widget()` method.

```python
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

from withtreebuilder import WithTreeBuilder


class KivyTreeBuilder(WithTreeBuilder):
    def __init__(self):
        super(KivyTreeBuilder, self).__init__()

    def add_child(self, parent, child):
        """Kivy widgets has a children field, too. But we do not want to use them.
        Instead, we use the recommended 'add_widget' method."""
        parent.add_widget(child)

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

```


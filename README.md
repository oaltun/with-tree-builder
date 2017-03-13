# with-tree-builder
This small library demonstrates how trees can be built using Python's with keyword.

Compare this:
```python
node('root',
    [node('child0'),
     node('child1'),
     node('child2',[
        node('child3')]])
```   
 With this:
 ```python
 with node('root'):
    with node('child0') as c: self.child0 = c  # Allows getting references to wanted nodes.
    with node('child1'): pass
    with node('child2'):
        # Any python code...
        with node('child3'): pass
 ```   
 Much easier to write and read. You can visualise the tree, just like Python code. Allows getting references to tree nodes. Allows arbitrary Python code to be written between node additions. And this is all Python, syntax checking, editor support, etc. are all already there.
 
Following is a full example of building a generic tree using with-tree-builder:
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

And following is a full simple Kivy application. Notice how a new 'add_child' is provided in KivyTreeBuilder class.

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


from contextlib import contextmanager


class WithTreeBuilder(object):
    def __init__(self):
        self.stack = list()
        self.parent = None

    @contextmanager
    def __call__(self, child):
        # If there is a parent, add child to it
        if self.parent:
            self.add_child(self.parent, child)

        # Push old parent to the stack. Make self the parent.
        self.stack.append(self.parent)
        self.parent = child

        # Let stuff be in the 'with' block
        yield child

        # Bring back the old parent
        self.parent = self.stack.pop()

    def add_child(self, parent, child):
        """Here we assume the nodes of your tree has a 'list()' of children.
        Override this method if needed. See the KivyTreeBuilder for an example
        of this."""
        parent.children.append(child)


class Node(object):
    def __init__(self, data=None):
        super(Node, self).__init__()
        self.data = data
        self.children = list()


class KivyTreeBuilder(WithTreeBuilder):
    def __init__(self):
        super(KivyTreeBuilder, self).__init__()

    def add_child(self, parent, child):
        """Kivy widgets has a children field, too. But we do not want to use them.
        Instead, we use the recommended 'add_widget' method."""
        parent.add_widget(child)

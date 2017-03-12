from withtreebuilder import WithTreeBuilder, Node


class MyTree(Node):
    def __init__(self,data):
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
# with-tree-builder
Demonstrates how trees can be built using Python's with keyword.

See the example files.

Why would one do something like this? 

Compare this:

node('root',
    [node('child0'),
     node('child1'),
     node('child2',[
        node('child3')]])
        
 With this:
 
 with node('root'):
    with node('child0') as c: self.child0 = c  # Allows getting references to wanted nodes.
    with node('child1'): pass
    with node('child2'):
        # Any python code...
        with node('child3'): pass
        
 Much easier to write and read. You can visualise the tree, just like Python code. Allows getting references to tree nodes. Allows arbitrary Python code to be written between node additions. And this is all Python, syntax checking, editor support, etc. are all already there.
 

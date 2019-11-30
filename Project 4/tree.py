class TreeNode:

    def __init__(self, name, parent=None):
        super(TreeNode, self).__init__()
        self.name = name
        self.parent = parent
        self.child = {}

    def get_child(self, name):
        return self.child.get(name)

    def get_parent(self):
        return self.parent

    def add_child(self, obj):
        if isinstance(obj, TreeNode):
            self.child[obj.name] = obj
            obj.parent = self
        else:
            self.child[obj] = None

    def del_child(self, name):
        if name in self.child:
            del self.child[name]

    def arrive_node(self, path, create=False):
        path = path if isinstance(path, list) else path.split()
        current = self
        for i in path:
            if i not in current.child.keys():
                if create:
                    current.add_child(i)
                else:
                    return None
            current = current.get_child(i)

        return current

    def show_tree(self):
        global public_string
        public_string = self.name
        def print_branch(treenode, degree):
            if isinstance(treenode, TreeNode):
                for item in treenode.child.keys():
                    #print((degree + 1) * '\t' + item)
                    global public_string
                    public_string += (degree + 1) * '----' + item + '\n'
                    print_branch(treenode.get_child(item), degree + 1)

        print_branch(self, 0)

        return public_string

    def list_children(self):
        childlist = []
        for item in self.child.keys():
            childlist.append(item)

        return childlist

    def print_path(self):
        path = []
        current = self
        res = ''
        while current != None:
            path.append(current.name)
            current = current.parent
        for i in range(len(path)):
            res += ('/' + path[-(i+1)])
        return res

if __name__ == '__main__':
    test = TreeNode('~')
    test.add_child('level_1_file')
    test.add_child(TreeNode('level_1_dic'))
    res = test.arrive_node(['level_1_dic'])
    res.add_child(TreeNode('level_2_dic'))
    print('Test add and arrive')
    test.show_tree()
    print('---------------')
    print('Test arrive exception')
    tmp = test.arrive_node(['level_?_dic'])
    print(tmp)
    print('---------------')
    print('Test list children')
    test.list_children()
    # print(res.arrive_node('level_2_dic').get_parent().name)
    print('---------------')
    print('Test pwd')
    res.print_path()
    res = res.arrive_node('level_2_dic')
    res.print_path()
    print('---------------')
    print('Test del')
    test.del_child('level_1_dic')
    test.show_tree()

import tree


def run_command(string, root: tree.TreeNode, current: tree.TreeNode):
    command = string.split(' ')
    function_name = command[0]

    if function_name == 'ls':
        if len(command) == 1:
            current.list_children()
        else:
            path = command[1].split('/')
            tmp = root.arrive_node(path)
            if tmp is None:
                print('No such path.')
            else:
                tmp.list_children()

    elif function_name == 'cd':
        if len(command) == 1:
            print('Path is needed.')
        else:
            path = command[1].split('/')
            tmp = root.arrive_node(path)
            if tmp is None:
                print('No such path.')
            else:
                current = tmp

    elif function_name == 'pwd':
        current.print_path()

    elif function_name == 'mkdir':
        if len(command) == 1:
            print('Path is needed.')
        else:
            current.add_child(tree.TreeNode(command[1]))

    elif function_name == 'touch':
        if len(command) == 1:
            print('Path is needed.')
        else:
            current.add_child(command[1])

    elif function_name == 'rm':
        if len(command) == 1:
            print('Path is needed.')
        else:
            current.del_child(command[1])

    elif function_name == 'tree':
        root.show_tree()

    else:
        print('Command not found.')

    return current

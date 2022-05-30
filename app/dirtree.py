import re


class DirNode(list):
    def __init__(self, level, index, long_tag, short_tag):
        super().__init__()
        self.parent = None
        self.level = level
        self.index = index
        self.long_tag = long_tag
        self.short_tag = short_tag
        self.path = None

    def part_repr(self):
        return f"{self.level}, {self.index}, {self.long_tag}, {self.short_tag}"

    def append(self, tl):
        tl.parent = self
        list.append(self, tl)

    def path_string(self):
        return ''.join(self.path)

    def long_path_string(self):
        node = self
        pth = []
        while node.parent is not None:
            pth.append(node.long_tag)
            node = node.parent
        pth.reverse()
        return '/'.join(pth)


def read_tree_line(the_tree):
    non_space = re.compile(r'\S')
    indent = 0
    for idx, line in enumerate(the_tree.splitlines()):
        mo = non_space.search(line)
        if mo is None:
            spa = 0
        else:
            spa = mo.start()
            if indent == 0:
                indent = spa
            line = line[spa:]
        line = line.strip()
        if not line:
            continue
        if indent != 0:
            spa = int(spa / indent)
        try:
            long_, short = line.split(',')
        except ValueError:
            long_ = line
            short = line[0]
        yield DirNode(spa, idx, long_, short.strip())


def parse_tree(the_tree):
    tree_root = DirNode(0, -1, 'root', 'h')
    tree_root.path = ['h']
    tree_as_path_dict = {}
    current_indent = 0
    node = tree_root
    path = []
    last = None
    for tl in read_tree_line(the_tree):
        if tl.level > current_indent:
            node = last
            path.append(last.short_tag)
        elif tl.level < current_indent:
            while node.parent is not None:
                node = node.parent
                path.pop()
                if node.level < tl.level:
                    break
        tl.path = path[:]
        tl.path.append(tl.short_tag)
        tree_as_path_dict[tl.path_string()] = tl
        node.append(tl)
        last = tl
        current_indent = last.level
    return tree_root, tree_as_path_dict


def read_tree(tree_file_name):
    with open(tree_file_name) as directory_fh:
        directory_tree = directory_fh.read()
    return parse_tree(directory_tree)

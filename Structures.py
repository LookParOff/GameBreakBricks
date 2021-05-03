import random


class Tree2D:
    def __init__(self, x=None, y=None, value=None):
        self.root = None
        if x is not None and y is not None:
            self.root = Node(x, y, value)
            self.root.level = 0

    def __eq__(self, other):
        # for tests
        stackForTree1 = [self.root]
        stackForTree2 = [other.root]
        while len(stackForTree1) != 0 and len(stackForTree2) != 0:
            node1 = stackForTree1.pop()
            node2 = stackForTree2.pop()
            if node1 != node2:
                return False
            if node1 is None:
                continue
            stackForTree1.append(node1.left_link)
            stackForTree2.append(node2.left_link)
            stackForTree1.append(node1.right_link)
            stackForTree2.append(node2.right_link)
        if len(stackForTree1) == len(stackForTree2) == 0:
            return True
        return False

    def search(self, x, y):
        level = 0
        node = self.root
        if node is None:
            return None
        while node.x != x or node.y != y:
            if level % 2 == 0:
                if x < node.x:
                    node = node.left_link
                else:
                    node = node.right_link
            else:
                if y < node.y:
                    node = node.left_link
                else:
                    node = node.right_link
            level += 1
            if node is None:
                return None
        return node

    def insert(self, x, y, value=None):
        if self.root is None:
            self.root = Node(x, y, value)
            self.root.level = 0
            return
        node = self.root
        node_to_insert = Node(x, y, value)
        level = 0
        while True:
            if level % 2 == 0:
                if x < node.x:
                    node_to_insert.xur = node.x
                else:
                    node_to_insert.xbl = node.x

                if x < node.x and node.left_link is not None:
                    node = node.left_link
                elif x >= node.x and node.right_link is not None:
                    node = node.right_link
                elif x < node.x and node.left_link is None:
                    node.left_link = node_to_insert
                    node_to_insert.father = node
                    node_to_insert.level = level + 1
                    break
                elif x >= node.x and node.right_link is None:
                    node.right_link = node_to_insert
                    node_to_insert.father = node
                    node_to_insert.level = level + 1
                    break
            else:
                if y < node.y:
                    node_to_insert.yur = node.y
                else:
                    node_to_insert.ybl = node.y

                if y < node.y and node.left_link is not None:
                    node = node.left_link
                elif y >= node.y and node.right_link is not None:
                    node = node.right_link
                elif y < node.y and node.left_link is None:
                    node.left_link = node_to_insert
                    node_to_insert.father = node
                    node_to_insert.level = level + 1
                    break
                elif y >= node.y and node.right_link is None:
                    node.right_link = node_to_insert
                    node_to_insert.father = node
                    node_to_insert.level = level + 1
                    break
            level += 1

    def insert_list(self, list_of_points: list, value=None):
        random.shuffle(list_of_points)  # this almost certainly make binary tree balanced
        for point in list_of_points:
            self.insert(point[0], point[1], value)

    def delete(self, x, y, node=None):
        if node is None:
            node = self.search(x, y)
        if node is None:
            return
        if node.left_link is None and node.right_link is None:
            # if node is leaf
            if node.father is None:
                self.root = None
                return
            if node.father.level % 2 == 0:
                if x < node.father.x:
                    node.father.left_link = None
                else:
                    node.father.right_link = None
            else:
                if y < node.father.y:
                    node.father.left_link = None
                else:
                    node.father.right_link = None
            node.father = None
            return
        if node.right_link is not None:
            # if we have right son
            node_to_replace_to_del = node.right_link.__find_min__(node.level + 1, node.level % 2)  # this node will delete after
            node_to_replace = node_to_replace_to_del.__copy__()  # find new node, to replace deletable node
        else:
            # we do not have right son
            node_to_replace_to_del = node.left_link.__find_min__(node.level + 1, node.level % 2)  # this node will delete after
            node_to_replace = node_to_replace_to_del.__copy__()  # find new node, to replace deletable node
        node_to_replace.left_link = node.left_link
        node_to_replace.right_link = node.right_link

        if node.father is None:
            node_to_replace.father = None
            node_to_replace.level = 0
            self.root = node_to_replace
        else:
            # say to father, that i am a new son
            node_to_replace.father = node.father
            node_to_replace.level = node.father.level + 1
            if node.father.level % 2 == 0:
                if node_to_replace.x < node.father.x:
                    node.father.left_link = node_to_replace
                else:
                    node.father.right_link = node_to_replace
            else:
                if node_to_replace.y < node.father.y:
                    node.father.left_link = node_to_replace
                else:
                    node.father.right_link = node_to_replace

        if node_to_replace.left_link is not None:
            node_to_replace.left_link.father = node_to_replace
        if node_to_replace.right_link is not None:
            node_to_replace.right_link.father = node_to_replace

        if node_to_replace.right_link is None:
            node_to_replace.right_link = node_to_replace.left_link
            node_to_replace.left_link = None
        # delete node, we alredy placed it in new place
        self.delete(x=node_to_replace_to_del.x, y=node_to_replace_to_del.y, node=node_to_replace_to_del)
        return

    def request_of_area(self, x0, y0, radius):
        # return list of points, which inside of circle with center (x0, y0) and radius
        points = []  # list of points, in circle
        stack = [self.root]
        while len(stack) != 0:
            node = stack.pop()
            if node is None:
                continue
            # if x0 - radius <= node.x <= x0 + radius and y0 - radius <= node.y <= y0 + radius:  # rectangle
            #     points.append((node.x, node.y))
            if (x0 - node.x)**2 + (y0 - node.y)**2 <= radius**2:
                points.append((node.x, node.y, node.value))
            if node.xur < x0 - radius or node.yur < y0 - radius or x0 + radius < node.xbl or y0 + radius < node.ybl:
                # all subtree with root node is not in circle
                continue
            else:
                # some points can be in circle
                stack.append(node.left_link)
                stack.append(node.right_link)
        return points


class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value  # some info to store in Node
        self.level = None  # level of node in tree, count from root
        self.father = None
        self.left_link = None
        self.right_link = None
        # values for request_of_area. Subtree with this node is located in a rectangle with this coordinates:
        self.xbl = -float("inf")  # bottom left
        self.ybl = -float("inf")
        self.xur = +float("inf")  # upper right
        self.yur = +float("inf")
        # TODO we can also in root store big rectangle, in which located all points in whole tree

    def __getitem__(self, item):
        if item == 0:
            return self.x
        return self.y

    def __copy__(self):
        return Node(self.x, self.y, self.value)

    def __eq__(self, other):
        # for tests
        if other is None:
            return False
        if self.x == other.x and self.y == other.y and \
                self.father == other.father and self.level == other.level:
            return True
        return False

    def __find_min__(self, level, component):
        # TODO maybe we can store in each node minimum node it this subtree?
        # find min in subtree with root root.
        # level- on which level of main tree node is.
        # component- x or y we search minimum. 0- x; 1- y
        stack = [(self, level)]
        min_node = self
        while len(stack) != 0:
            node, level_of_node = stack.pop()
            if node is None:
                continue
            if node[component] < min_node[component]:
                min_node = node
            if level_of_node % 2 == component:
                stack.append((node.left_link, level_of_node + 1))
            else:
                stack.append((node.left_link, level_of_node + 1))
                stack.append((node.right_link, level_of_node + 1))
        return min_node


if __name__ == "__main__":
    print()

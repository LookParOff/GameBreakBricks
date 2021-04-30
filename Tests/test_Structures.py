from unittest import TestCase
from Structures import Tree2D


class TestTree2D(TestCase):
    def __create_test_tree1__(self):
        tree = Tree2D()
        tree.insert(10, 10)
        tree.insert(6, 30)
        tree.insert(12, 10)
        tree.insert(1, 1)
        tree.insert(5, 40)
        tree.insert(15, 6)
        tree.insert(12, 35)
        return tree

    def test_eq1(self):
        tree = Tree2D()
        tree.insert(10, 10)
        tree.insert(6, 30)
        tree.insert(12, 10)

        corr_tree = Tree2D()
        corr_tree.insert(10, 10)
        corr_tree.insert(6, 30)
        corr_tree.insert(12, 10)
        self.assertEqual(corr_tree, tree)

    def test_eq2(self):
        tree = Tree2D()
        corr_tree = Tree2D()
        self.assertEqual(corr_tree, tree)

    def test_eq3(self):
        tree = Tree2D(1, 1)
        corr_tree = Tree2D()
        corr_tree.insert(1, 1)
        self.assertEqual(corr_tree, tree)

    def test_search1(self):
        tree = self.__create_test_tree1__()
        corr_tree = self.__create_test_tree1__()

        node = tree.search(6, 30)
        self.assertEqual(node, corr_tree.root.left_link)
        node = tree.search(10, 10)
        self.assertEqual(node, corr_tree.root)

    def test_search2(self):
        tree = self.__create_test_tree1__()
        corr_tree = self.__create_test_tree1__()

        node = tree.search(12, 35)
        self.assertEqual(node, corr_tree.root.right_link.right_link)
        node = tree.search(5, 40)
        self.assertEqual(node, corr_tree.root.left_link.right_link)

    def test_delete1(self):
        tree = Tree2D()
        tree.delete(0, 0)
        corr_tree = Tree2D()
        self.assertEqual(tree, corr_tree)

    def test_delete2(self):
        tree = Tree2D(10, 10)
        tree.delete(10, 10)
        corr_tree = Tree2D()
        self.assertEqual(tree, corr_tree)

    def test_delete3(self):
        tree = Tree2D()
        tree.insert(10, 10)
        tree.insert(6, 30)
        tree.insert(12, 10)
        tree.delete(6, 30)

        corr_tree = Tree2D()
        corr_tree.insert(10, 10)
        corr_tree.insert(12, 10)
        self.assertEqual(tree, corr_tree)

    def test_delete4(self):
        # we have right son
        tree = self.__create_test_tree1__()
        tree.delete(10, 10)
        corr_tree = Tree2D()
        corr_tree.insert(12, 10)
        corr_tree.insert(6, 30)
        corr_tree.insert(12, 35)
        corr_tree.insert(1, 1)
        corr_tree.insert(5, 40)
        corr_tree.insert(15, 6)
        self.assertEqual(tree, corr_tree)

    def test_delete5(self):
        # we have right son
        tree = self.__create_test_tree1__()
        tree.delete(6, 30)
        corr_tree = Tree2D()
        corr_tree.insert(10, 10)
        corr_tree.insert(5, 40)
        corr_tree.insert(12, 10)
        corr_tree.insert(1, 1)
        corr_tree.insert(15, 6)
        corr_tree.insert(12, 35)
        self.assertEqual(tree, corr_tree)

    def test_delete6(self):
        # we do not have right son, but have left
        tree = Tree2D()
        tree.insert(10, 10)
        tree.insert(6, 30)
        tree.insert(12, 10)
        tree.insert(1, 1)
        tree.insert(15, 6)
        tree.insert(12, 35)
        tree.delete(6, 30)

        corr_tree = Tree2D()
        corr_tree.insert(10, 10)
        corr_tree.insert(1, 1)
        corr_tree.insert(12, 10)
        corr_tree.insert(15, 6)
        corr_tree.insert(12, 35)
        self.assertEqual(tree, corr_tree)

    def test_delete7(self):
        # we do not have right son, but have left
        tree = Tree2D()
        tree.insert(10, 10)
        tree.insert(6, 30)
        tree.insert(5, 40)
        tree.insert(1, 1)
        tree.delete(10, 10)

        corr_tree = Tree2D()
        corr_tree.insert(1, 1)
        corr_tree.insert(6, 30)
        corr_tree.insert(5, 40)
        self.assertEqual(tree, corr_tree)

    def test_delete8(self):
        # we do not have right son, but have left
        tree = Tree2D()
        tree.insert(10, 10)
        tree.insert(6, 30)
        tree.insert(5, 40)
        tree.insert(1, 1)
        tree.insert(0, 40)
        tree.delete(10, 10)

        corr_tree = Tree2D()
        corr_tree.insert(0, 40)
        corr_tree.insert(6, 30)
        corr_tree.insert(1, 1)
        corr_tree.insert(5, 40)
        self.assertEqual(tree, corr_tree)

    def test_delete9(self):
        tree = Tree2D(10, 20)
        tree.insert(6, 30)
        tree.insert(20, 8)
        tree.insert(7, 15)
        tree.insert(5, 40)
        tree.insert(15, 6)
        tree.insert(12, 10)
        tree.insert(1, 1)
        tree.insert(4, 50)
        tree.insert(7, 40)
        tree.insert(10, 10)
        tree.insert(12, 35)
        tree.insert(3, 20)
        tree.insert(15, 15)
        print(tree)
        tree.delete(20, 8)
        tree.delete(7, 15)
        tree.delete(10, 20)
        print(tree)

        corr_tree = Tree2D(10, 10)
        corr_tree.insert(6, 30)
        corr_tree.insert(12, 10)
        corr_tree.insert(1, 1)
        corr_tree.insert(5, 40)
        corr_tree.insert(15, 6)
        corr_tree.insert(12, 35)
        corr_tree.insert(3, 20)
        corr_tree.insert(4, 50)
        corr_tree.insert(7, 40)
        corr_tree.insert(15, 15)
        self.assertEqual(tree, corr_tree)

    def test_of_request_area0_0(self):
        tree = self.__create_test_tree1__()
        points = tree.request_of_area(100, 100, 1)
        corr_points = []
        self.assertListEqual(points, corr_points)

    def test_of_request_area0_1(self):
        tree = Tree2D()
        points = tree.request_of_area(100, 100, 1)
        corr_points = []
        self.assertListEqual(points, corr_points)

    def test_of_request_area0_2(self):
        tree = Tree2D(1, 1)
        points = tree.request_of_area(1, 1, 1)
        corr_points = [(1, 1)]
        self.assertListEqual(points, corr_points)

    def test_of_request_area0_3(self):
        tree = Tree2D(1, 1)
        points = tree.request_of_area(10, 1, 1)
        corr_points = []
        self.assertListEqual(points, corr_points)

    def test_of_request_area1_1(self):
        tree = self.__create_test_tree1__()
        points = tree.request_of_area(10, 10, 10)
        corr_points = [(10, 10), (12, 10), (15, 6)]
        self.assertListEqual(points, corr_points)

    def test_of_request_area1_2(self):
        tree = self.__create_test_tree1__()
        points = tree.request_of_area(10, 10, 22)
        corr_points = [(10, 10), (12, 10), (15, 6), (6, 30), (1, 1)]
        self.assertListEqual(points, corr_points)

    def test_of_request_area1_3(self):
        tree = self.__create_test_tree1__()
        points = tree.request_of_area(10, 10, 4)
        corr_points = [(10, 10), (12, 10)]
        self.assertListEqual(points, corr_points)

    def test_of_request_area1_4(self):
        tree = self.__create_test_tree1__()
        points = tree.request_of_area(0, 0, 2**0.5)
        corr_points = [(1, 1)]
        self.assertListEqual(points, corr_points)

    def test_of_request_area1_5(self):
        tree = self.__create_test_tree1__()
        points = tree.request_of_area(0, 0, 1.999**0.5)
        corr_points = []
        self.assertListEqual(points, corr_points)

    def test_of_request_area2_1(self):
        tree = self.__create_test_tree1__()
        points = tree.request_of_area(9, 33, 3)
        corr_points = []
        self.assertListEqual(points, corr_points)

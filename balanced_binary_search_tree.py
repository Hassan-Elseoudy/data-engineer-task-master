from datetime import datetime
from math import inf

INT_MAX = inf


class Record:
    def __init__(self, status, date):
        self.status = status
        self.date = date


# binary tree node
class Node:
    def __init__(self, d: Record):
        self.data = d
        self.left = None
        self.right = None


class BST:
    """
     function to convert sorted array to a balanced BST.
    input : sorted array of integers
    output: root node of balanced BST
    """
    def array_to_bst(self, arr: []) -> Node:
        if not arr:
            return None

        # find middle
        mid = (len(arr)) / 2

        # make the middle element the root
        root = Node(arr[mid])

        # left subtree of root has all
        # values <arr[mid]
        root.left = self.array_to_bst(arr[:mid])

        # right subtree of root has all
        # values >arr[mid]
        root.right = self.array_to_bst(arr[mid + 1:])
        return root

    """This function is used to find floor of a key"""
    def get_nearest_status(self, root: Node, key: datetime):
        if not root:
            return INT_MAX

        """ If root.data is equal to key """
        if root.data == key:
            return root.data.status

        """ If root.data is greater than the key """
        if root.data.date > key:
            return self.get_nearest_status(root.left, key)

        """ Else, the floor may lie in right subtree
        or may be equal to the root"""
        floor_value = self.get_nearest_status(root.right, key)
        return floor_value if (floor_value <= key) else root.data.status

    # A utility function to print the preorder
    # traversal of the BST
    def pre_order(self, node: Node):
        if not node:
            return

        print(node.data)
        self.pre_order(node.left)
        self.pre_order(node.right)
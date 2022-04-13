import enum
from datetime import datetime

DATE_MAX = datetime.max


class UserStatus(enum.Enum):
    PAYING = "paying",
    CANCELLED = "cancelled"
    NOT_PAYING = "not_paying"
    NA = "NA"


USER_STATUS_DICT = {
    "paying": UserStatus.PAYING,
    "cancelled": UserStatus.CANCELLED,
    "not_paying": UserStatus.NOT_PAYING,
    "NA": UserStatus.NA,
}


class Record:
    def __init__(self, status: UserStatus, created_at: datetime):
        self.status = status
        self.created_at = created_at


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
            return Node(Record(UserStatus.NOT_PAYING, DATE_MAX))

        # Find Middle
        mid = len(arr) // 2

        # Middle element the root
        root = Node(arr[mid])

        # Left subtree of root has all values < arr[mid]
        root.left = self.array_to_bst(arr[:mid])

        # Right subtree of root has all values > arr[mid]
        root.right = self.array_to_bst(arr[mid + 1:])

        return root

    """This function is used to find floor of a key"""
    def get_nearest_status(self, root: Node, key: datetime) -> Node:
        if not root:
            return Node(d=Record(created_at=DATE_MAX, status=UserStatus.NOT_PAYING))

        search_key = root.data.created_at

        """ If root.data is equal to key """
        if search_key == key:
            return root

        """ If root.data is greater than the key """
        if search_key > key:
            return self.get_nearest_status(root.left, key)

        """ Else, the floor may lie in right subtree or may be equal to the root"""
        floor_value = self.get_nearest_status(root.right, key)

        return floor_value if (floor_value.data.created_at <= key) else root

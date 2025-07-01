# search.py

class Node:
    def __init__(self, key):
        self.key = key
        self.values = []
        self.left = None
        self.right = None

    def __len__(self):
        # count my values ...
        size = len(self.values)
        # ... plus everything in the left subtree
        if self.left is not None:
            size += len(self.left)
        # ... plus everything in the right subtree
        if self.right is not None:
            size += len(self.right)
        return size

    def lookup(self, key):
        """
        Return the list of values for exactly this key,
        or [] if not found in this subtree.
        """
        if key == self.key:
            return self.values
        elif key < self.key and self.left is not None:
            return self.left.lookup(key)
        elif key > self.key and self.right is not None:
            return self.right.lookup(key)
        else:
            return []


class BST:
    def __init__(self):
        self.root = None

    def add(self, key, val):
        # first node?
        if self.root is None:
            self.root = Node(key)

        curr = self.root
        while True:
            if key < curr.key:
                # go left
                if curr.left is None:
                    curr.left = Node(key)
                curr = curr.left

            elif key > curr.key:
                # go right
                if curr.right is None:
                    curr.right = Node(key)
                curr = curr.right

            else:
                # found matching key
                break

        # attach the value
        curr.values.append(val)

    def __dump(self, node):
        if node is None:
            return
        # for ascending order: left, then self, then right
        self.__dump(node.left)
        print(node.key, ":", node.values)
        self.__dump(node.right)

    def dump(self):
        self.__dump(self.root)

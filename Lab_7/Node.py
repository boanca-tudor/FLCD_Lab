class Node:
    def __init__(self, value):
        self.father = -1
        self.sibling = -1
        self.value = value
        self.index = 0

    def __str__(self):
        return str(self.index) + " " + str(self.value) + " " + str(self.father) + " " + str(self.sibling)


class NodeHelper:
    def __init__(self, value):
        self.father = None
        self.sibling = -1
        self.value = value
        self.index = 0
        self.level = 0

from .DfgNode import DfgNode


class Concat(DfgNode):

    def __init__(self, children: list[DfgNode]):
        self.children = children

    def __call__(self, *args, **kwargs):
        result = []

        for child in self.children:
            result += child(*args, **kwargs)

        return result

    def children(self):
        return self.children

    def description(self):
        return "Concat"

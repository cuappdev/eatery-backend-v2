from api.dfg.nodes.DfgNode import DfgNode
from api.dfg.nodes.system.ConvertToJson import ConvertToJson
from api.dfg.nodes.system.ConvertFromJson import EateryFromJson
from api.dfg.nodes.system.LeftMerge import LeftMerge

class LeftMergeEateries(DfgNode):

    def __init__(self, left: DfgNode, right: DfgNode):
        def comparator(left, right):
            if left["id"] == right["id"]:
                return 0
            elif left["id"] == None:
                return -1
            elif right["id"] == None:
                return 1
            elif left["id"] < right["id"]:
                return -1
            else:
                return 1
        self.macro = EateryFromJson(
            LeftMerge(
                ConvertToJson(left),
                ConvertToJson(right),
                comparator
            )
        )

    def children(self):
        return self.macro.children()

    def __call__(self, *args, **kwargs):
        return self.macro(*args, **kwargs)

    def description(self):
        return "LeftMergeEateries"

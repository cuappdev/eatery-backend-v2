from api.dfg.nodes.DfgNode import DfgNode

from api.dfg.nodes.system.ConvertToJson import ConvertToJson
from api.dfg.nodes.system.ConvertFromJson import EventFromJson
from api.dfg.nodes.system.LeftMerge import LeftMerge

# Merges two lists of objects, combining objects with matching IDs (keys of object in left array have precedence if
# conflict)
class LeftMergeEvents(DfgNode):
    def __init__(self, left: DfgNode, right: DfgNode):
        def comparator(left, right):
            left_val = (left["canonical_date"], left["description"])
            right_val = (right["canonical_date"], right["description"])
            if left_val == right_val:
                return 0
            elif left_val < right_val:
                return -1
            else:
                return 1
        self.macro = EventFromJson(
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
        return "LeftMergeEvents"
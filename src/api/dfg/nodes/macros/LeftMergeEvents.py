from api.dfg.nodes.DfgNode import DfgNode
from api.dfg.nodes.system.ConvertFromJson import EventFromJson
from api.dfg.nodes.system.ConvertToJson import ConvertToJson
from api.dfg.nodes.system.LeftMerge import LeftMerge


class LeftMergeEvents(DfgNode):
    def __init__(self, left: DfgNode, right: DfgNode, attr_lst: list[str]):
        def comparator(left, right):
            left_val = [left.get(attr) for attr in attr_lst]
            right_val = [right.get(attr) for attr in attr_lst]
            if left_val == right_val:
                return 0
            else:
                return 1

        self.macro = EventFromJson(
            LeftMerge(ConvertToJson(left), ConvertToJson(right), comparator)
        )

    def children(self):
        return self.macro.children()

    def __call__(self, *args, **kwargs):
        return self.macro(*args, **kwargs)

    def description(self):
        return "LeftMergeEvents"

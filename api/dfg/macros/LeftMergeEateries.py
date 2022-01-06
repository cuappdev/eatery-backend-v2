from api.dfg.DfgNode import DfgNode
from api.dfg.EateryToJson import EateryToJson
from api.dfg.EateryFromJson import EateryFromJson
from api.dfg.LeftMergeById import LeftMergeById


class LeftMergeEateries(DfgNode):

    def __init__(self, left: DfgNode, right: DfgNode):
        self.macro = EateryFromJson(
            LeftMergeById(
                EateryToJson(left),
                EateryToJson(right)
            )
        )

    def children(self):
        return self.macro.children()

    def __call__(self, *args, **kwargs):
        return self.macro(*args, **kwargs)

    def description(self):
        return "LeftMergeEateries"

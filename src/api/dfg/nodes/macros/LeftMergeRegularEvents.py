from api.dfg.nodes.DfgNode import DfgNode
from api.dfg.nodes.macros.LeftMergeEvents import LeftMergeEvents


class LeftMergeRegularEvents(LeftMergeEvents):
    """
    Merges two lists of Event objects, regardless of how they were generated
    """

    def __init__(self, left: DfgNode, right: DfgNode):
        super().__init__(left, right, ["canonical_date", "description"])

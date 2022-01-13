from api.dfg.nodes.DfgNode import DfgNode
from typing import Callable, TypeVar, Any
from functools import cmp_to_key
T = TypeVar("T")

# Merges two lists of objects, combining objects with matching IDs (keys of object in left array have precedence if
# conflict)
class LeftMerge(DfgNode):

    def __init__(self, left: DfgNode, right: DfgNode, comparator: Callable[[T, T], int]):
        self.left = left
        self.right = right
        self.comparator = comparator

    def children(self):
        return [self.left, self.right]

    def __call__(self: Any, *args, **kwargs):
        left_lst = sorted(self.left(*args, **kwargs), key=cmp_to_key(self.comparator))
        right_lst = sorted(self.right(*args, **kwargs), key=cmp_to_key(self.comparator))
        left_json = _pop_first(left_lst)
        right_json = _pop_first(right_lst)
        merged_lst = []
        while left_json is not None and right_json is not None:
            if self.comparator(left_json, right_json) == 0:
                merged_json = {}
                for key in right_json:
                    if right_json[key] is not None:
                        merged_json[key] = right_json[key]
                for key in left_json:
                    if left_json[key] is not None:
                        merged_json[key] = left_json[key]
                merged_lst.append(merged_json)
                left_json = _pop_first(left_lst)
                right_json = _pop_first(right_lst)
            elif self.comparator(left_json, right_json) < 0:
                merged_lst.append(left_json)
                left_json = _pop_first(left_lst)
            else:
                merged_lst.append(right_json)
                right_json = _pop_first(right_lst)
        if left_json is not None:
            merged_lst.append(left_json)
        if right_json is not None:
            merged_lst.append(right_json)
        merged_lst.extend(left_lst)
        merged_lst.extend(right_lst)
        return merged_lst

    def description(self):
        return "LeftMerge"


def _pop_first(lst: list):
    try:
        return lst.pop(0)
    except IndexError:
        return None

from api.dfg.DfgNode import DfgNode


# Merges two lists of objects, combining objects with matching IDs (keys of object in left array have precedence if
# conflict)
class LeftMergeById(DfgNode):

    def __init__(self, left: DfgNode, right: DfgNode):
        self.left = left
        self.right = right

    def children(self):
        return [self.left, self.right]

    def __call__(self, *args, **kwargs):
        left_lst = sorted(self.left(*args, **kwargs), key=lambda x: x["id"])
        right_lst = sorted(self.right(*args, **kwargs), key=lambda x: x["id"])
        left_json = _pop_first(left_lst)
        right_json = _pop_first(right_lst)
        merged_lst = []
        while left_json is not None and right_json is not None:
            if left_json["id"] == right_json["id"]:
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
            elif left_json["id"] < right_json["id"]:
                merged_lst.append(left_json)
                left_json = _pop_first(left_lst)
            else:
                merged_lst.append(right_json)
                right_json = _pop_first(right_lst)
        merged_lst.extend(left_lst)
        merged_lst.extend(right_lst)
        return merged_lst

    def description(self):
        return "LeftMergeById"


def _pop_first(lst: list):
    try:
        return lst.pop(0)
    except IndexError:
        return None

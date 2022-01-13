from dfg.nodes.DfgNode import DfgNode
from util.json import success_json, error_json


class DictResponseWrapper(DfgNode):

    def __init__(self, child: DfgNode, re_raise_exceptions: bool = False):
        self.child = child
        self.re_raise_exceptions = re_raise_exceptions

    def __call__(self, *args, **kwargs):
        try:
            return success_json(self.child(*args, **kwargs))

        except Exception as e:
            if self.re_raise_exceptions:
                raise e
            return error_json(str(e))

    def description(self):
        return "DictResponseWrapper"

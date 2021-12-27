from api.dfg.DfgNode import DfgNode


class DictResponseWrapper(DfgNode):

    def __init__(self, child: DfgNode, re_raise_exceptions: bool = False):
        self.child = child
        self.re_raise_exceptions = re_raise_exceptions

    def __call__(self, *args, **kwargs):
        try:
            return {
                "success": True,
                "data": self.child(*args, **kwargs),
                "error": None
            }

        except Exception as e:
            if self.re_raise_exceptions:
                raise e

            return {
                "success": False,
                "data": None,
                "error": str(e)
            }

    def children(self):
        return [self.child]

    def description(self):
        return "DictResponseWrapper"

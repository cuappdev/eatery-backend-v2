from src.dfg.DfgNode import DfgNode


class DictResponseWrapper(DfgNode):

    def __init__(self, child: DfgNode):
        self.child = child

    def __call__(self, *args, **kwargs):
        try:
            return {
                "success": True,
                "data": self.child(*args, **kwargs),
                "error": None
            }

        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }

    def children(self):
        return [self.child]

    def description(self):
        return "DictResponseWrapper"

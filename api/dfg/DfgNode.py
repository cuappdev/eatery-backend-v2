class DfgNode:

    def __call__(self, *args, **kwargs):
        raise Exception()

    def children(self):
        return []

    def description(self):
        raise Exception()

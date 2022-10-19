"""from event.datatype.Event import Event
from typing import Union
from api.dfg.nodes.DfgNode import DfgNode


class EventFromJson(DfgNode):
    def __init__(self, child: DfgNode):
        self.child = child

    def __call__(self, *args, **kwargs):
        result = self.child(*args, **kwargs)
        return EventFromJson.from_json(result, *args, **kwargs)

    def children(self):
        return [self.child]

    @staticmethod
    def from_json(obj: Union[list, dict], *args, **kwargs):
        if isinstance(obj, list):
            return [EventFromJson.from_json(elem, *args, **kwargs) for elem in obj]
        else:
            return Event.from_json(obj)

    def description(self):
        return "ConvertFromJson"""
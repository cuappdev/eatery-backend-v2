import time

from api.dfg.DfgNode import DfgNode
from typing import Optional

from api.dfg.util.ConvertToJson import ConvertToJson


class DataSnapshot:

    def __init__(self, args, kwargs, data, time):
        self.data = data
        self.recorded_time = time
        self.args = args
        self.kwargs = kwargs

    def is_usable_snapshot(self, oldest_possible_time, args, kwargs):
        return args == self.args and kwargs == self.kwargs and self.recorded_time >= oldest_possible_time

    def get_data(self):
        return self.data

    def to_json(self):
        return ConvertToJson.to_json(self.data, *self.args, **self.kwargs)

    def get_recorded_time(self):
        return self.recorded_time


class InMemoryCache(DfgNode):

    def __init__(self, child, expiration: float = 3600, max_size: int = 5):
        self.child = child
        self.expiration = expiration
        self.max_size = max_size
        self.snapshots: list[DataSnapshot] = []

    def current_time(self):
        return time.time()

    def fifo_index(self):
        if len(self.snapshots) == 0:
            return None
        oldest_snapshot_time = self.snapshots[0].get_recorded_time()
        oldest_snapshot_index = 0
        for i in range(1, len(self.snapshots)):
            if self.snapshots[i].get_recorded_time() < oldest_snapshot_time:
                oldest_snapshot_time = self.snapshots[i].get_recorded_time()
                oldest_snapshot_index = i
        return oldest_snapshot_index

    def __call__(self, *args, **kwargs):
        should_reload = kwargs.get("reload")
        for snapshot in self.snapshots:
            if not should_reload and snapshot.is_usable_snapshot(self.current_time() - self.expiration, args, kwargs):
                print(f"{self}: Returning from cache")
                return snapshot.get_data()

        print(f"{self}: Fetching data")
        new_snapshot = DataSnapshot(args, kwargs, self.child(*args, **kwargs), self.current_time())
        if len(self.snapshots) < self.max_size:
            self.snapshots.append(new_snapshot)
        else:
            index_to_replace = self.fifo_index()
            self.snapshots[index_to_replace] = new_snapshot
        return new_snapshot.get_data()

    def to_json(self, *args, **kwargs):
        for snapshot in self.snapshots:
            if snapshot.is_usable_snapshot(self.current_time() - self.expiration, args, kwargs):
                return snapshot.to_json()
        return ConvertToJson.to_json(self.child(*args, **kwargs), *args, **kwargs)

    def description(self):
        return "InMemoryCache"

import time

from src.dfg.DfgNode import DfgNode


class InMemoryCache(DfgNode):

    def __init__(self, child, expiration: float = 60):
        self.child = child
        self.expiration = expiration
        self.last_refresh_time = None
        self.last_refresh_data = None

    def current_time(self):
        return time.time()

    def is_expired(self):
        return (
            self.last_refresh_data is None
            or self.last_refresh_time is None
            or (self.current_time() - self.last_refresh_time) > self.expiration
        )

    def __call__(self, *args, **kwargs):
        if self.is_expired():
            self.last_refresh_data = self.child()
            self.last_refresh_time = self.current_time()
            print(f"{self}: Fetching data")

        else:
            print(f"{self}: Returning from cache")

        return self.last_refresh_data

    def children(self):
        return [self.child]


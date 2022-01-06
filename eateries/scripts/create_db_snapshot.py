
from eateries.models import EateryStore


def create_snapshot():
    eateries = EateryStore.objects.all()


create_snapshot()
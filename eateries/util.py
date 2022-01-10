from enum import Enum

class SnapshotFileName(Enum):
    EATERY_STORE = "eatery_store.txt"
    EXCEPTION_STORE = "exception_store.txt"
    CATEGORY_STORE = "category_store.txt"
    MENU_STORE = "menu_store.txt"
    ITEM_STORE = "item_store.txt"
    SUBITEM_STORE = "subitem_store.txt"
    CATEGORY_ITEM_ASSOCIATION = "category_item_association.txt"
    EVENT_SCHEDULE = "event_schedule.txt"
    DAY_OF_WEEK_EVENT_SCHEDULE = "day_of_week_event_schedule.txt"
    DATE_EVENT_SCHEDULE = "date_event_schedule.txt"
    CLOSED_EVENT_SCHEDULE = "closed_event_schedule.txt"
    TRANSACTION_HISTORY = "transaction_history.txt"
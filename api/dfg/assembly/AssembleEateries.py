# takes in api_data, google_sheets data, and stubs, and generates a list[Eatery]

from typing import Optional, TypeVar
from api.dfg.DfgNode import DfgNode
from api.dfg.assembly.datatype.Eatery import Eatery
from api.dfg.preparation.datatype.EateryStub import EateryStub
from api.dfg.preparation.datatype.Event import Event
from api.dfg.preparation.datatype.OverrideEatery import OverrideEatery
from api.dfg.preparation.datatype.CornellDiningEatery import CornellDiningEatery
from api.dfg.preparation.datatype.OverrideEvent import OverrideEvent

T = TypeVar('T')

class AssembleEateries(DfgNode):

    def __init__(self, stubs: DfgNode, cornell_dining: DfgNode, override: DfgNode):
        self.stubs = stubs
        self.cornell_dining = cornell_dining
        self.override = override

    def __call__(self, *args, **kwargs):
        assembled_eateries = []
        eatery_stubs = self.stubs(*args, **kwargs)
        cornell_dining_eateries = self.cornell_dining(*args, **kwargs)
        override_eateries = self.override(*args, **kwargs)

        for stub in eatery_stubs:
            cornell_dining_eatery = next((eatery for eatery in cornell_dining_eateries if eatery.name == stub.name), None)
            override_eatery = next((eatery for eatery in override_eateries if eatery.name == stub.name), None)
            assembled_eateries.append(AssembleEateries.preparation_to_eatery(
                stub=stub, 
                cornell_dining_eatery=cornell_dining_eatery,
                override_eatery=override_eatery
            ))
        return assembled_eateries

    @staticmethod
    def preparation_to_eatery(
        stub: EateryStub, 
        cornell_dining_eatery: Optional[CornellDiningEatery], 
        override_eatery: Optional[OverrideEatery]
    ) -> Eatery:
        return Eatery(
            id=stub.id,
            name=stub.name,
            campus_area=AssembleEateries.fetch_field_precedence_first(
                None if override_eatery is None else override_eatery.campus_area,
                None if cornell_dining_eatery is None else cornell_dining_eatery.campus_area),
            events=AssembleEateries.events_with_precedence(
                None if override_eatery is None else override_eatery.known_events,
                None if cornell_dining_eatery is None else cornell_dining_eatery.known_events),
            latitude=AssembleEateries.fetch_field_precedence_first(
                None if override_eatery is None else override_eatery.latitude,
                None if cornell_dining_eatery is None else cornell_dining_eatery.latitude),
            longitude=AssembleEateries.fetch_field_precedence_first(
                None if override_eatery is None else override_eatery.longitude,
                None if cornell_dining_eatery is None else cornell_dining_eatery.longitude),
            payment_methods=AssembleEateries.fetch_field_precedence_first(
                None if override_eatery is None else override_eatery.payment_methods,
                None if cornell_dining_eatery is None else cornell_dining_eatery.payment_methods),
            location=AssembleEateries.fetch_field_precedence_first(
                None if override_eatery is None else override_eatery.location,
                None if cornell_dining_eatery is None else cornell_dining_eatery.location),
            online_order=AssembleEateries.fetch_field_precedence_first(
                None if override_eatery is None else override_eatery.online_order,
                None if cornell_dining_eatery is None else cornell_dining_eatery.online_order),
            online_order_url=AssembleEateries.fetch_field_precedence_first(
                None if override_eatery is None else override_eatery.online_order_url,
                None if cornell_dining_eatery is None else cornell_dining_eatery.online_order_url)
        )
    
    @staticmethod
    def events_with_precedence(
        optional_override_events: Optional[list[OverrideEvent]],
        optional_cornell_dining_events: Optional[list[Event]]
    ):
        override_events = [] if optional_override_events is None else optional_override_events
        cornell_dining_events = [] if optional_cornell_dining_events is None else optional_cornell_dining_events
        events = []

        for event in cornell_dining_events:
            potential_override_event = next((override_event for override_event in override_events if
                override_event.canonical_date == event.canonical_date and 
                override_event.description == event.description 
            ), None)
            if potential_override_event is not None:
                events.append(event)
        for event in override_events:
            if event.exists:
                events.append(Event(
                    description=event.description,
                    canonical_date=event.canonical_date,
                    start_timestamp=event.start_timestamp,
                    end_timestamp=event.end_timestamp,
                    menu=event.menu
                ))
        return events

    @staticmethod
    def fetch_field_precedence_first(
        primary: Optional[T],
        secondary: Optional[T],
    ) -> Optional[T]:
        return secondary if primary is None else primary

    def description(self):
        return "AssembleEateries"

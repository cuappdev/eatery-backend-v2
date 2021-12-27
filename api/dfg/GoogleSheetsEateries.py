import datetime
import json
import os
import re
from typing import Optional

import pytz

from api.datatype.Cafe import Cafe
from api.datatype.CafeEvent import CafeEvent
from api.datatype.CafeMenu import CafeMenu
from api.datatype.MenuItem import MenuItem
from api.dfg.DfgNode import DfgNode

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleSheetsEateries(DfgNode):

    def __init__(
            self,
            spreadsheet_id: str,
            external_eateries_path: str = 'static_sources/external_eateries.json',
            credentials_path: str = 'credentials.json',
            cached_token_path: str = 'token.json'
    ):
        self.spreadsheet_id = spreadsheet_id
        self.external_eateries_path = external_eateries_path
        self.credentials_path = credentials_path
        self.token_cache_path = cached_token_path

    def __call__(self, *args, **kwargs):
        eateries = []

        with open(self.external_eateries_path) as f:
            json_eateries = json.load(f)["eateries"]

            for json_eatery in json_eateries:
                eateries.append(self.cafe_from_json(json_eatery))

        return eateries

    def cafe_from_json(self, json_eatery: dict) -> Cafe:
        return Cafe(
            name=json_eatery["name"],
            campus_area=json_eatery["campusArea"]["descrshort"],
            events=self.cafe_events_from_google_sheets(
                table_name=json_eatery["name"],
            ),
            latitude=json_eatery["coordinates"]["latitude"],
            longitude=json_eatery["coordinates"]["longitude"],
            menu=GoogleSheetsEateries.cafe_menu_from_json(
                json_eatery["diningItems"]
            )
        )

    def cafe_events_from_google_sheets(
            self,
            table_name: str,
    ) -> list[CafeEvent]:
        scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
        creds = None
        if os.path.exists(self.token_cache_path):
            creds = Credentials.from_authorized_user_file(self.token_cache_path, scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes)
                creds = flow.run_local_server(port=0)

            with open(self.token_cache_path, "w") as token:
                token.write(creds.to_json())

        try:
            service = build("sheets", "v4", credentials=creds)
            sheet = service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"{table_name}!A:C"
            ).execute()
            values = result.get("values", [])

        except HttpError as err:
            print(f"{self}: {err}")
            return []

        events = []
        for row in values:
            event = self.parse_row(row)
            if event is not None:
                events.append(event)

        return events

    def parse_row(self, row: list[str]) -> Optional[CafeEvent]:
        if len(row) != 3:
            return None

        try:
            date = datetime.date.fromisoformat(row[0])

        except ValueError:
            return None

        start_time = self.parse_time(row[1])
        end_time = self.parse_time(row[2])

        if start_time is None or end_time is None:
            return None

        return CafeEvent(
            canonical_date=date,
            start_timestamp=GoogleSheetsEateries.timestamp_combined(date, start_time),
            end_timestamp=GoogleSheetsEateries.timestamp_combined(date, end_time)
        )

    def parse_time(self, time_str: str) -> Optional[datetime.time]:
        # time_str is like 10:00 AM or 3:00 PM
        match = re.fullmatch(r'([0-9]?[0-9]):([0-9][0-9]) ([AP]M)', time_str)
        if not match:
            return None

        hours = int(match.group(1))
        minutes = int(match.group(2))
        is_pm = match.group(3) == "pm"
        try:
            return datetime.time(
                hour=hours + (12 if is_pm else 0),
                minute=minutes
            )

        except Exception as e:
            print(f"{self}: e")
            return None

    @staticmethod
    def cafe_menu_from_json(json_dining_items: list) -> CafeMenu:
        items = []

        for json_dining_item in json_dining_items:
            items.append(MenuItem(
                healthy=json_dining_item["healthy"],
                name=json_dining_item["item"]
            ))

        return CafeMenu(items=items)

    @staticmethod
    def timestamp_combined(date: datetime.date, time: datetime.time):
        """
        Returns the Unix (UTC) timestamp of the combined (date, time) in the
        New York timezone.
        """

        tz = pytz.timezone('America/New_York')
        return int(tz.localize(datetime.datetime.combine(date, time)).timestamp())

    def description(self):
        return "ExternalEateries"


if __name__ == "__main__":
    from api.dfg.EateryToJson import EateryToJson

    dfg = EateryToJson(GoogleSheetsEateries(
        spreadsheet_id="1ImfeTUA6I1Ub-aavgIW53Pf7EVB694f1294NPSCRd5c",
    ))

    print(json.dumps(dfg(), indent=2))

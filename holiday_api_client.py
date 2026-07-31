# This file job is to fetch real public holidays from a free external service called the Nager.date API

import re
import requests
from holiday import Holiday


class HolidayAPIClient:
    # To Fetch public holidays from the Nager.Date API
    def __init__(self):
        self.base_url = "https://date.nager.at/api/v3"

    def validate_year(self, year):
        year = str(year)  
        year = year.strip()  
        # year must be a 4-digit number starting with 19 or 20
        if not re.fullmatch(r"(19|20)\d{2}", year):
            raise ValueError(f"Invalid year '{year}'. Enter a 4-digit year like 2026.")
        return int(year)

    def get_holidays(self, country, year):
        year = self.validate_year(year)
        # builds the exact address the Nager.Date API expects, e.g.
        # https://date.nager.at/api/v3/PublicHolidays/2026/NG
        url = f"{self.base_url}/PublicHolidays/{year}/{country.code}"

        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to reach the holiday API: {e}")

        if response.status_code == 404:
            # 404 means the country code isn't in their database - bad input
            raise ValueError(f"No holiday data found for '{country.code}'.")
        if response.status_code != 200:
            # any other non-200 means something's wrong on their end, not ours
            raise ConnectionError(f"API request failed (status {response.status_code}).")

        holidays = []
        data = response.json()  # turns the raw JSON text into a Python list of dicts
        for item in data:
            date = item.get("date")
            name = item.get("name")
            local_name = item.get("localName")
            types = item.get("types") or []  # e.g. ["Public"] or ["Public", "Bank"]
            if types:
                # our Holiday class wants one string, so join the list, e.g. "Public, Bank"
                holiday_type = ", ".join(types)
            else:
                holiday_type = "Public"
            holiday = Holiday(date, name, local_name, holiday_type)
            holidays.append(holiday)
        return holidays

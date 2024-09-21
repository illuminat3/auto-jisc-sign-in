import requests
from DTOs.Lecture import *

class JiscEventsExtractor:
    def __init__(self, headers) -> None:
        self.url = "https://api.la.jisc.ac.uk/event/timetable"
        self.headers = headers
    
    def GetEvents(self):
        response = requests.get(self.url, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f"Failed to fetch events: {response.status_code}")
        
        events_data = response.json()
        lectures = []

        for date, events in events_data.items():
            for event in events:
                # Check if the event is not cancelled
                if event.get("isCancelled", False):
                    continue

                lecture = Lecture(
                    time=event.get("startDateTime"),
                    name=event.get("name"),
                    eventId=event.get("eventId")
                )
                lectures.append(lecture)
        
        return lectures

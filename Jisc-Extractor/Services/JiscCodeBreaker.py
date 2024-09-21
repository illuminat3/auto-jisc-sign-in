import requests
import threading

class JiscCodeBreaker:
    def __init__(self, headers, eventId, searchValueLow = 0, searchValueHigh = 999999, threadCount = 10):
        self.eventId = eventId
        self.threadCount = threadCount
        self.headers = headers
        self.searchValueLow = 0
        self.searchValueHigh = searchValueHigh
        self.searchValue = searchValueLow
        self.url = f"https://api.la.jisc.ac.uk/event/lookup/{str(self.searchValue).zfill(6)}?id={eventId}"

    def GetCode():
        pass
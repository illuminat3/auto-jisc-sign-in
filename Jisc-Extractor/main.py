from Services.JiscTokenExtractor import *
from Services.JiscEventsExtractor import *

def Main() -> None:
    jiscTokenExtractor = JiscTokenExtractor()

    headers = jiscTokenExtractor.GetJiscHeaders()

    jiscEventsExtractor = JiscEventsExtractor(headers)

    lectures = jiscEventsExtractor.GetEvents()

    for lecture in lectures:
        print(lecture)
    

if __name__ == '__main__':
    Main()
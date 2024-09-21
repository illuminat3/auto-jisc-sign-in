from Services.Setup import *
from Services.JiscTokenExtractor import *
from Services.JiscEventsExtractor import *
from Services.JiscCodeBreaker import *

def Main() -> None:
    setup = Setup("Jisc-Extractor/requirements.txt")

    setup.install_packages

    jiscTokenExtractor = JiscTokenExtractor()

    headers = jiscTokenExtractor.GetJiscHeaders()

    jiscEventsExtractor = JiscEventsExtractor(headers)
    lectures = jiscEventsExtractor.GetEvents()

    jiscCodeBreaker = JiscCodeBreaker(headers, lectures[0])
    jiscCodeBreaker.GetCode()  
    

if __name__ == '__main__':
    Main()
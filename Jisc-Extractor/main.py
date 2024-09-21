from Services.Setup import *
from Services.JiscTokenExtractor import *
from Services.JiscEventsExtractor import *

def Main() -> None:
    setup = Setup("Jisc-Extractor/requirements.txt")

    setup.install_packages

    jiscTokenExtractor = JiscTokenExtractor()

    headers = jiscTokenExtractor.GetJiscHeaders()

    jiscEventsExtractor = JiscEventsExtractor(headers)

    lectures = jiscEventsExtractor.GetEvents()

    for lecture in lectures:
        print(lecture)
    

if __name__ == '__main__':
    Main()
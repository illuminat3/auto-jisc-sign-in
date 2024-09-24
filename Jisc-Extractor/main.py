from Services.Setup import *
from Services.JiscTokenExtractor import *
from Services.JiscEventsExtractor import *
from Services.JiscCodeBreaker import *
from Services.SystemProfiler import *

def Main() -> None:

    # DO NOT COMMIT WITH ACTUAL VALUES!!!
    username = ""
    password = ""
    email = "" 
    # DO NOT COMMIT WITH ACTUAL VALUES!!!

    setup = Setup("Jisc-Extractor/requirements.txt")
    systemProfiler = SystemProfiler()

    setup.install_packages()

    jiscTokenExtractor = JiscTokenExtractor(username, password, email)

    headers = jiscTokenExtractor.GetJiscHeaders()

    jiscEventsExtractor = JiscEventsExtractor(headers)
    lectures = jiscEventsExtractor.GetEvents()

    threadCount = 4 * systemProfiler.GetCoreCount() 

    jiscCodeBreaker = JiscCodeBreaker(headers, lectures[0],jiscTokenExtractor=jiscTokenExtractor, threadCount=threadCount)
    jiscCodeBreaker.GetCode()  
    

if __name__ == '__main__':
    Main()
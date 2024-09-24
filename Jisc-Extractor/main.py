from Services.Setup import *

def Main() -> None:

    # DO NOT COMMIT WITH ACTUAL VALUES!!!
    username = ""
    password = ""
    email = "" 
    # DO NOT COMMIT WITH ACTUAL VALUES!!!

    systemProfiler = SystemProfiler()

    jiscTokenExtractor = JiscTokenExtractor(username, password, email)

    headers = jiscTokenExtractor.GetJiscHeaders()

    jiscEventsExtractor = JiscEventsExtractor(headers)
    lectures = jiscEventsExtractor.GetEvents()

    threadCount = 4 * systemProfiler.GetCoreCount() 

    jiscCodeBreaker = JiscCodeBreaker(headers, lectures[0],jiscTokenExtractor=jiscTokenExtractor, threadCount=threadCount)
    jiscCodeBreaker.GetCode()  
    

if __name__ == '__main__':
    setup = Setup("Jisc-Extractor/requirements.txt")

    setup.install_packages()

    from Services.JiscTokenExtractor import *
    from Services.JiscEventsExtractor import *
    from Services.JiscCodeBreaker import *
    from Services.SystemProfiler import *

    Main()
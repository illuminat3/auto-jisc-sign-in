from Services.Setup import *

def Main() -> None:

    load_dotenv()

    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    email = os.getenv("EMAIL")

    if not all([username, password, email]):
        raise ValueError("Missing one or more required environment variables: USERNAME, PASSWORD, EMAIL")

    systemProfiler = SystemProfiler()

    jiscTokenExtractor = JiscTokenExtractor(username, password, email)

    headers = jiscTokenExtractor.GetJiscHeaders()

    jiscEventsExtractor = JiscEventsExtractor(headers)
    lectures = jiscEventsExtractor.GetEvents()

    threadCount = 4 * systemProfiler.GetCoreCount() 

    jiscCodeBreaker = JiscCodeBreaker(headers, lectures[0], jiscTokenExtractor=jiscTokenExtractor, threadCount=threadCount)
    jiscCodeBreaker.GetCode()  
    

if __name__ == '__main__':
    setup = Setup("Jisc-Extractor/requirements.txt")

    setup.install_packages()

    from Services.JiscTokenExtractor import *
    from Services.JiscEventsExtractor import *
    from Services.JiscCodeBreaker import *
    from Services.SystemProfiler import *
    from dotenv import load_dotenv
    import os

    Main()
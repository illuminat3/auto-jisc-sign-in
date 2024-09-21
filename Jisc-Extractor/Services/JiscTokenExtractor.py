from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

class JiscTokenExtractor:
    def __init__(self):
        self.options = Options()
        self.options.headless = True 
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.execute_cdp_cmd("Network.enable", {})
    
    def GetJiscHeaders(self):
        try:
            login_url = "https://studygoal.jisc.ac.uk/login/"
            target_url = "https://student.la.jisc.ac.uk/home"

            self.driver.get(login_url)
            
            while True:
                time.sleep(1)
                if self.driver.current_url == target_url:
                    break
            
            print("User has reached the target page.")
            
            cookies = self.driver.get_cookies()
            cookie_header = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
            
            headers = {
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-GB,en;q=0.5",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Cookie": cookie_header,
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0"
            }
            
            return headers
        
        finally:
            self.driver.quit()
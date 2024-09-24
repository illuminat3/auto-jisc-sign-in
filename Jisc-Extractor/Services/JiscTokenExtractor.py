from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

class JiscTokenExtractor:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.login_url = "https://student.la.jisc.ac.uk/"
        self.target_url = "https://student.la.jisc.ac.uk/home"
    
    def _setup(self):
        self.options = Options()
        self.options.add_argument('--window-position=0,3000') # hide the browser by making it appear offscreen (im such a good programmer)
        self.options.add_argument('--no-sandbox') 
        self.options.add_argument('--disable-dev-shm-usage')  
        self.options.add_argument('--headless') 
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.driver.execute_cdp_cmd("Network.enable", {})
        self.driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})


    def GetJiscHeaders(self):
        try:
            self._setup()
            self._load_auth_login()
            self._enter_email_and_continue()
            self._enter_credentials()
            self._wait_for_home_page()
            headers = self._get_header()
            
            return headers
        
        finally:
            self.driver.quit()

    def _load_auth_login(self):
        self.driver.get(self.login_url)
    
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Log in']]"))
        )
        login_button.click()

    def _enter_email_and_continue(self):
        email_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(self.email)

        continue_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "continue"))
        )
        continue_button.click()

    def _enter_credentials(self):
        username_input = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "j_username"))
        )
        username_input.send_keys(self.username)

        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "j_password"))
        )
        password_input.send_keys(self.password)

        submit_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "credentials_input_submit"))
        )
        submit_button.click()
    
    def _wait_for_home_page(self):
        while True:
            time.sleep(1)
            if self.driver.current_url == self.target_url:
                print("User has reached the target page.")
                break

    def _get_header(self):
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
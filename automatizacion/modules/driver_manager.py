from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

class DriverManager():

    def __init__(
            self,
            init_user_agent:bool=True
            ):
        
        self.__driver = self.init_driver(init_user_agent)
        self.__driver.set_page_load_timeout(120)
    
    def init_driver(self, intit_user_agent: bool = True, usar_remote: bool = False, headless: bool = False):
        

        chromeOptions = Options()

        # 1. User-Agent aleatorio
        if intit_user_agent:
            random_user_agent = UserAgent().random
            chromeOptions.add_argument(f"user-agent={random_user_agent}")

        # 2. Configuraciones comunes
        chromeOptions.add_argument("--disable-search-engine-choice-screen")
        chromeOptions.add_argument("--disable-password-manager-reauthentication")
        chromeOptions.add_argument("--disable-save-password-bubble")
        chromeOptions.add_argument("--disable-blink-features=AutomationControlled")
        chromeOptions.add_experimental_option("excludeSwitches", ["enable-automation"])
        chromeOptions.add_experimental_option("prefs", {"credentials_enable_service": False})

        # 3. Modo headless opcional
        # if headless:
        #     chromeOptions.add_argument("--headless=new")
        #     chromeOptions.add_argument("--disable-gpu")
        #     chromeOptions.add_argument("--no-sandbox")
        #     chromeOptions.add_argument("--disable-dev-shm-usage")
        #     chromeOptions.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=chromeOptions)

        # 6. Confirmación
        print("User-Agent:", driver.execute_script("return navigator.userAgent;"))
        print("Driver session_id:", driver.session_id)

        driver.implicitly_wait(5)
        return driver
    
    def get_driver(self):
        return self.__driver
    
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, ElementNotInteractableException,WebDriverException,NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class SeleniumLibrerias():
    
    @staticmethod
    def ir_y_verificar_url(driver:webdriver.Chrome, url:str):
        count = 0
        while True:
            if count == 3:
                raise Exception(f"url no confirmada, url = '{url}'")
            try:
                if driver.current_url == url:
                    break
                
                driver.get(url)
                WebDriverWait(driver, 7).until(EC.url_to_be(url))
                break
            except:
                x += 1
                driver.get(url)
                print(f"[ERROR] no se accedio a la url {count}")
                continue
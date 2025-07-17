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

from librerias.generales_librerias import GeneralesLibrerias as gn_l

class SeleniumLibrerias():
    
    @staticmethod
    def esperar_carga(driver:webdriver.Chrome,by:By,value:str,ec:EC, implicitly_wait:int=5):
        try:
            wait = WebDriverWait(driver,5)
            
            # ESTE ES EL TIEMPO QUE SE TARDA EN HACER LA BUSQUEDA CON EL 'find_element' ANTES DEL RAISE
            driver.implicitly_wait(implicitly_wait)
            while True:
                try:
                    driver.find_element(by, value)
                    wait.until(ec((by, value)))
                    break
                except TimeoutException:
                    print("Cargando...")
                    continue
                except NoSuchElementException:
                    # No encuentra la pantalla de carga
                    break
        except:
            raise
        finally:
            driver.implicitly_wait(5)

    @staticmethod
    def asignar_directorio_descargas(driver:webdriver.Chrome, ruta:str, crear_carpeta:bool=True):
        driver.command_executor._commands["send_chrome_command"] = ("POST","/session/$sessionId/chromium/send_command")        
        
        params = {
            "cmd" : "Page.setDownloadBehavior",
            "params":{
                "behavior" : "allow",
                "downloadPath": ruta
                }
            }

        driver.execute("send_chrome_command",params)

        if crear_carpeta:
            gn_l.crear_carpeta(ruta)

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
                count += 1
                driver.get(url)
                print(f"[ERROR] no se accedio a la url {count}")
                continue
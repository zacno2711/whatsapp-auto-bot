from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from automatizacion.modules.driver_manager import DriverManager
from librerias.selenium_librerias import SeleniumLibrerias as slm_l
from librerias.generales_librerias import GeneralesLibrerias as gn_l

class WhatsApp_slm(DriverManager):
    def __init__(self):
        self.url_wpp_web = "https://web.whatsapp.com/"
        super().__init__(init_user_agent=False)
    
    def espera_carga_pantalla(self):
        slm_l.esperar_carga(
            driver = self.get_driver(),
            by = By.NAME,
            value = ""
        )

    def abrir_wpp(self):
        driver = self.get_driver()
        slm_l.ir_y_verificar_url(driver,self.url_wpp_web)

        print("WatsApp Abierto")
        print("Validando estado de la sesion")

        self.espera_carga_pantalla()
        

        
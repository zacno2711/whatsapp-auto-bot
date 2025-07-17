from automatizacion.modules.driver_manager import DriverManager
from librerias.selenium_librerias import SeleniumLibrerias as slm_l

class WhatsApp_slm(DriverManager):
    def __init__(self):
        self.url_wpp_web = "https://web.whatsapp.com/"
        super().__init__(init_user_agent=True)

    def abrir_wpp(self):
        driver = self.get_driver()
        slm_l.ir_y_verificar_url(driver,self.url_wpp_web)
        print("WatsApp Abierto")
        print("Validando estado de la sesion")
        
        
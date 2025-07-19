import time
import traceback
import urllib.parse

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
            ec=EC.presence_of_element_located,
            value = "progress"
        )

    def abrir_wpp(self):
        driver = self.get_driver()
        slm_l.ir_y_verificar_url(driver,self.url_wpp_web)

        print("[INFO] WatsApp Abierto")
        print("[INFO] Validando estado de la sesion")
        
        
        count = 0
        while True:
            if count == 5:
                raise Exception("no se pudo abrir wpp, por cantidad de intentos de lectura de QR fallidos")
            count += 1
            try:
                elemento_qr = driver.find_element(By.XPATH,'//canvas[contains(@aria-label,"QR")]')
                print(f"[INFO] QR presente, se debe escanear par continuar, {count}")
                print("[INFO] escanea el QR para continuar")
                input("[INPUT] Oprime ENTER despues de escanear")
            except:
                print("[INFO] QR escaneado con exito")
                time.sleep(10)
                break
          
        
        self.espera_carga_pantalla()

        try:
            boton_popup_continuar = driver.find_element(By.XPATH,'//div[@data-animate-modal-body]//button[contains(.,"Continue")]')
            print("[WARNING] existe un elemento con informacion")
            slm_l.click_by_js(driver,boton_popup_continuar)
            print("[SUCCESS] popup cerrado")
        except:
            pass

        print("[SUCCESS] WhatsApp Cargado con exito")

    def elegir_boton_lateral_izquierdo_wpp(self,nombre_boton):
        """Nombres validos = ["Settings","Profile","Chats","Status","Channels","Communities"]"""
        def validar_aria_pressed(elemento_boton):
            aria_pressed = slm_l.obtener_atributos_elemento(driver,elemento_boton).get("aria-pressed",None)
            print(f"aria-pressed = {aria_pressed}")
            if not aria_pressed:
                raise Exception(f"el boton '//button[@aria-label={nombre_boton}' no tiene el atributo 'aria-pressed'")
            if aria_pressed == "false":
                return False
            elif aria_pressed == "true":
                print(f"[SUCCESS] boton '{nombre_boton}' seleccionado")
                return True
            raise Exception("el valor del atributo 'aria_pressed' no es valido")
        
        driver = self.get_driver()
        elemento_boton = driver.find_element(By.XPATH,f'//button[@aria-label="{nombre_boton}"]')

        count = 0
        while not validar_aria_pressed(elemento_boton):
            if count == 3:
                raise Exception(f"No se pudo elegir el boton lateral izquierdo '{nombre_boton}', {count}")
            count +=1
            slm_l.click_by_js(driver,elemento_boton)
            time.sleep(3)

    def cerrar_sesion_wpp(self):
        self.elegir_boton_lateral_izquierdo_wpp("Settings")
        try:
            driver = self.get_driver()
            elemento_boton_log_out = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//span[@data-icon="exit-refreshed"]')))
            slm_l.click_by_js(driver, elemento_boton_log_out)
            elemento_2_boton_log_out = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//div[h1[contains(.,"Log out?")]]//button[contains(.,"Log out")]')))
            slm_l.click_by_js(driver, elemento_2_boton_log_out)
            print("[SUCCESS] WatsApp deslogueado correctamente")
        except Exception as e:
            print(traceback.print_exc())
            print("[WARNING] no se pudo cerrar sesion")
        
    def generar_link_whatsapp(self, numero_telefono: str, mensaje: str) -> str:
        """
        Genera un enlace directo a WhatsApp Web con el número y mensaje especificado.

        Args:
            numero_telefono (str): Número en formato internacional, sin '+', espacios ni guiones. Ej: '573001234567'
            mensaje (str): Texto que se quiere enviar

        Returns:
            str: URL lista para abrir en WhatsApp Web
        """
        def validar_numero_telefono(numero_telefono: str) -> str:
            numero_limpio = numero_telefono.replace("+", "").strip()

            if not numero_limpio.isdigit():
                raise ValueError(f"El número de teléfono '{numero_telefono}' no es válido. Revisar.")

            return numero_limpio
            
        numero_telefono = validar_numero_telefono(numero_telefono)
        mensaje_codificado = urllib.parse.quote(mensaje)
        link = f"https://web.whatsapp.com/send?phone={numero_telefono}&text={mensaje_codificado}"
        return link 

    def enviar_mensaje_wpp(self,numero_telefono:str,mensaje:str,ruta_adjunto:str):
        link_wpp = self.generar_link_whatsapp(numero_telefono,mensaje)
        pass
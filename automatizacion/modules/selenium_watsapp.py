import time
import traceback
import urllib.parse
import inspect
from librerias.logger_config import get_logger

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from automatizacion.modules.driver_manager import DriverManager
from librerias.selenium_librerias import SeleniumLibrerias as slm_l
from librerias.generales_librerias import GeneralesLibrerias as gn_l

class WhatsApp_slm(DriverManager):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)
        self.url_wpp_web = "https://web.whatsapp.com/"
        super().__init__(init_user_agent=False)
    
    def espera_carga_pantalla(self):
        slm_l.esperar_carga(
            driver = self.get_driver(),
            by = By.XPATH,
            ec=EC.presence_of_element_located,
            value = "//progress"
        )

    def abrir_wpp(self):
        driver = self.get_driver()
        slm_l.ir_y_verificar_url(driver,self.url_wpp_web)

        self.logger.info("WatsApp Abierto")
        self.logger.info("Validando estado de la sesion")
        
        
        count = 0
        while True:
            if count == 5:
                e = "no se pudo abrir wpp, por cantidad de intentos de lectura de QR fallidos"
                self.logger.error(e)
                raise Exception(e)
            count += 1
            try:
                elemento_qr = driver.find_element(By.XPATH,'//canvas[contains(@aria-label,"QR")]')
                self.logger.info(f"QR presente, se debe escanear par continuar, {count}")
                self.logger.info("escanea el QR para continuar")
                input("[INPUT] Oprime ENTER despues de escanear")
            except:
                self.logger.info("✅ QR escaneado con exito")
                time.sleep(10)
                break
          
        
        self.espera_carga_pantalla()

        try:
            boton_popup_continuar = driver.find_element(By.XPATH,'//div[@data-animate-modal-body]//button[contains(.,"Continue")]')
            self.logger.warning("existe un popup")
            slm_l.click_by_js(driver,boton_popup_continuar)
            self.logger.info("✅ popup cerrado")
        except:
            pass

        self.logger.info("✅ WhatsApp Cargado con exito")

    def elegir_boton_lateral_izquierdo_wpp(self,nombre_boton):
        """Nombres validos = ["Settings","Profile","Chats","Status","Channels","Communities"]"""
        def validar_aria_pressed(elemento_boton):
            aria_pressed = slm_l.obtener_atributos_elemento(driver,elemento_boton).get("aria-pressed",None)
            if not aria_pressed:
                raise Exception(f"el boton '//button[@aria-label={nombre_boton}' no tiene el atributo 'aria-pressed'")
            if aria_pressed == "false":
                return False
            elif aria_pressed == "true":
                self.logger.info(f"✅ boton '{nombre_boton}' seleccionado")
                return True
            e = "el valor del atributo 'aria_pressed' no es valido"
            self.logger.error(e)
            raise ValueError(e)
        
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
            self.logger.info("✅ WatsApp deslogueado correctamente")
        except Exception as e:
            self.logger.exception(e)
            self.logger.warning("no se pudo cerrar sesion")

    @staticmethod
    def validar_y_limpiar_numero_telefono(numero_telefono: str) -> str:

        logger = get_logger(inspect.currentframe().f_code.co_name)
        if not numero_telefono:
            e = f"El número de teléfono esta vacio. Revisar."
            logger.error(e)
            raise ValueError(e)
        numero_limpio = numero_telefono.replace("+", "").strip()

        if not numero_limpio.isdigit():
            e = f"El número de teléfono '{numero_telefono}' no es válido. Revisar."
            logger.error(e)
            raise ValueError(e)

        return numero_limpio

    def generar_link_whatsapp(self, numero_telefono: str, mensaje: str = None) -> str:
        """
        Genera un enlace directo a WhatsApp Web con el número y mensaje especificado.

        Args:
            numero_telefono (str): Número en formato internacional, sin '+', espacios ni guiones. Ej: '573001234567'
            mensaje (str): Texto que se quiere enviar

        Returns:
            str: URL lista para abrir en WhatsApp Web
        """
        if mensaje:
            mensaje_codificado = urllib.parse.quote(mensaje)
            link = f"https://web.whatsapp.com/send?phone={numero_telefono}&text={mensaje_codificado}"
        else:
            link = f"https://web.whatsapp.com/send?phone={numero_telefono}"
        return link 

    def oprimir_boton_enviar(self):
        driver = self.get_driver()
        try:
            boton_enviar = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//span[@data-icon="wds-ic-send-filled"]')))
            slm_l.click_by_js(driver,boton_enviar)
            self.logger.info("Boton enviar oprimido")
        except Exception as e:
            e = f"al intentar oprimir el boton enviar, {e}"
            self.logger.exception(e)
            raise Exception(e)

    def enviar_mensaje_wpp(
            self,
            numero_telefono:str,
            mensaje:str = None ,
            # ruta_adjunto:str = None
            ):
        def validar_envio_mensaje():
            try:
                fraccion_mensaje_enviado = mensaje[:50].lower().strip().replace("*", "")
                ultimo_mensaje = driver.find_element(
                    By.XPATH,
                    '(//div[@class="copyable-text"]//span[contains(@class,"copyable-text")])[last()]'
                ).text.lower().strip()
                
                self.logger.info(f"Último mensaje detectado: '{ultimo_mensaje}'")
                self.logger.info(f"Fragmento del mensaje enviado: '{fraccion_mensaje_enviado}'")
                
                if fraccion_mensaje_enviado in ultimo_mensaje:
                    self.logger.info("✅ El mensaje fue enviado correctamente.")
                    return True
                else:
                    self.logger.error("❌ El fragmento del mensaje no coincide con el último mensaje recibido.")
                    return False

            except Exception as e:
                self.logger.error("❌ No se pudo validar el envío del mensaje. Posible diferencia entre lo esperado y lo recibido.")
                self.logger.exception(f"❌ [DETALLE ERROR] {e}")
                return False
        
        # if not mensaje and not ruta_adjunto: 
        #     raise Exception("Es necesario un mensaje o un adjunto para enviar el mensaje por wpp")
        
        driver = self.get_driver()
        numero_telefono = WhatsApp_slm.validar_y_limpiar_numero_telefono(numero_telefono)
        link_wpp = self.generar_link_whatsapp(numero_telefono,mensaje)
        driver.get(link_wpp)
        
        # if ruta_adjunto:
        #     try:
        #         input_file = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//input")))
        #         input_file.send_keys(ruta_adjunto)
        #         print("adjunto cargado en input")
        #     except Exception as e:
        #         raise Exception (f"No se pudo acceder al input para el adjunto, {e}")

        self.oprimir_boton_enviar()
        validar_envio_mensaje()
        
        
        
        

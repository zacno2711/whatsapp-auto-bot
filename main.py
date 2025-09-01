from automatizacion.modules.selenium_watsapp import WhatsApp_slm
from automatizacion.main.main_workflow import MainWorkflow
from automatizacion.templates_messages.templates import Templates

ruta_excel = r"C:\Users\juanp\Documents\proyecto_mensajes_asesores\cartera_prueba.xlsx"
wpp = MainWorkflow(
    ruta_excel=ruta_excel,
    nombre_asistente="Luisa Maria Humanes",
    nombre_asesor="Juan Pablo Zapata",
    ruta_carpeta_principal=r"C:\Users\juanp\Documents"
    )

wpp.enviar_mensajes_wpp(Templates.cartera)
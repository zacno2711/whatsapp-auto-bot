from automatizacion.modules.selenium_watsapp import WhatsApp_slm
from automatizacion.main.main_workflow import MainWorkflow
from automatizacion.templates_messages.templates import Templates


# mensaje_prueba = (
#     "Hola, este es un mensaje de prueba generado automáticamente para probar el funcionamiento del enlace de WhatsApp con un texto largo. "
#     "Queremos asegurarnos de que el mensaje se procese correctamente, sin errores, y que todo el contenido sea enviado adecuadamente. "
#     "Esto es especialmente útil cuando se requiere enviar información extensa, como instrucciones, detalles técnicos, listas de tareas, recordatorios "
#     "o cualquier otro tipo de contenido que pueda superar los límites de un mensaje tradicional. A continuación, seguimos escribiendo texto adicional "
#     "para completar los mil caracteres requeridos. Gracias por tu paciencia y colaboración. Si llegaste hasta aquí leyendo, te felicitamos por tu concentración. "
#     "Seguimos agregando más contenido para asegurar que se cumpla con el requisito de longitud. Este mensaje no contiene información personal ni confidencial, "
#     "y solo tiene como propósito hacer una prueba técnica. ¡Gracias por participar en esta prueba! Nos acercamos al final del mensaje. Ya casi llegamos. Un poco más... ¡y listo!"
# )
# ruta_archivo = r"C:\Users\juanp\Downloads\imagen.jpeg"

# slm_wpp = WhatsApp_slm()
# slm_wpp.abrir_wpp()
# url = slm_wpp.enviar_mensaje_wpp(
#     numero_telefono="573052428530",
#     mensaje=mensaje_prueba,
#     # ruta_adjunto=ruta_archivo
#     )
# print("prueba")

ruta_excel = r"C:\Users\juanp\Documents\proyecto_mensajes_asesores\cartera_prueba.xlsx"
wpp = MainWorkflow(
    ruta_excel=ruta_excel,
    nombre_asistente="Luisa Maria Humanes",
    nombre_asesor="Juan Pablo Zapata",
    ruta_carpeta_principal=r"C:\Users\juanp\Documents"
    )

wpp.enviar_mensajes_wpp(Templates.cartera)
from automatizacion.modules.selenium_watsapp import WhatsApp_slm

slm_wpp = WhatsApp_slm()
# slm_wpp.abrir_wpp()
mensaje_prueba = (
    "Hola, este es un mensaje de prueba generado automáticamente para probar el funcionamiento del enlace de WhatsApp con un texto largo. "
    "Queremos asegurarnos de que el mensaje se procese correctamente, sin errores, y que todo el contenido sea enviado adecuadamente. "
    "Esto es especialmente útil cuando se requiere enviar información extensa, como instrucciones, detalles técnicos, listas de tareas, recordatorios "
    "o cualquier otro tipo de contenido que pueda superar los límites de un mensaje tradicional. A continuación, seguimos escribiendo texto adicional "
    "para completar los mil caracteres requeridos. Gracias por tu paciencia y colaboración. Si llegaste hasta aquí leyendo, te felicitamos por tu concentración. "
    "Seguimos agregando más contenido para asegurar que se cumpla con el requisito de longitud. Este mensaje no contiene información personal ni confidencial, "
    "y solo tiene como propósito hacer una prueba técnica. ¡Gracias por participar en esta prueba! Nos acercamos al final del mensaje. Ya casi llegamos. Un poco más... ¡y listo!"
)

url = slm_wpp.generar_link_whatsapp("573052428530",mensaje_prueba)
print("prueba")
from automatizacion.modules.selenium_watsapp import WhatsApp_slm

mensaje_prueba = (
    "Hola, este es un mensaje de prueba generado automáticamente para probar el funcionamiento del enlace de WhatsApp con un texto largo. "
    "Queremos asegurarnos de que el mensaje se procese correctamente, sin errores, y que todo el contenido sea enviado adecuadamente. "
    "Esto es especialmente útil cuando se requiere enviar información extensa, como instrucciones, detalles técnicos, listas de tareas, recordatorios "
    "o cualquier otro tipo de contenido que pueda superar los límites de un mensaje tradicional. A continuación, seguimos escribiendo texto adicional "
    "para completar los mil caracteres requeridos. Gracias por tu paciencia y colaboración. Si llegaste hasta aquí leyendo, te felicitamos por tu concentración. "
    "Seguimos agregando más contenido para asegurar que se cumpla con el requisito de longitud. Este mensaje no contiene información personal ni confidencial, "
    "y solo tiene como propósito hacer una prueba técnica. ¡Gracias por participar en esta prueba! Nos acercamos al final del mensaje. Ya casi llegamos. Un poco más... ¡y listo!"
)
ruta_archivo = r"C:\Users\juanp\Downloads\imagen.jpeg"

slm_wpp = WhatsApp_slm()
slm_wpp.abrir_wpp()
url = slm_wpp.enviar_mensaje_wpp(
    numero_telefono="573052428530",
    mensaje=mensaje_prueba,
    # ruta_adjunto=ruta_archivo
    )
print("prueba")


# import pywhatkit as kit
# import datetime

# # Datos del contacto
# numero = "+573001234567"  # Número con código de país (ej: +57 para Colombia)
# mensaje = "Hola, esto es un mensaje automático con pywhatkit 😄"

# # Hora en la que se enviará (mínimo 1 minuto después de la hora actual)
# hora_actual = datetime.datetime.now()
# hora_envio = (hora_actual.hour, hora_actual.minute + 1)

# # Enviar mensaje
# kit.sendwhatmsg(numero, mensaje, hora_envio[0], hora_envio[1])
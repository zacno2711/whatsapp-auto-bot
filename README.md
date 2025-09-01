
# WHATSAPP-AUTO-BOT

This project allows you to send WhatsApp messages automatically using Selenium, without relying on third-party services like Twilio or external libraries that "control WhatsApp."

The bot opens WhatsApp Web, logs in with a QR code, and sends messages to the specified contacts. This makes it a lightweight and flexible solution for tasks such as:

- Automating reminders

- Sending bulk notifications

- Testing integrations without paid APIs

By leveraging the official WhatsApp Web interface, you keep full control of the process with no dependency on external providers.

## 📦 Prerequisites

Before running the project, make sure you have the following installed:

- Python 3.12.3

- Google Chrome (latest stable version)

- ChromeDriver matching your Chrome version

- Install dependencies with:

`pip install -r requirements.txt`

### ⚠️ Important:
Every time you start the project, you will need to scan the WhatsApp Web QR code.
This is done for security reasons and ensures that no session is stored on your machine.

## ✨ Features  

- ✅ **WhatsApp Web integration** → Works directly with the official WhatsApp Web interface.  
- ✅ **Secure QR login** → Requires QR scan on every startup for security.  
- ✅ **Single & bulk messaging** → Send individual or mass messages with ease.  
- ✅ **Advisor workflow ready** → Already adapted to send bulk messages for advisors (see `main.py` for the logic).  
- ✅ **Customizable logic** → Extend or modify the sending behavior to fit your needs.    
- ✅ **Lightweight & open-source** → No external APIs or paid services required. 
- ✅ **Message tracking** → Automatically generates a file with the delivery status of each message (success or error).

## ⚙️ Usage
### 1. Prepare your Excel file
- The project depends on an Excel file that contains the information required to send messages.

- The file must include the columns required by your chosen template.

- You can adapt the validation logic in:

`automatizacion/main/main_workflow.py `

`class MainWorkflow`

`method validar_df_info` 

### 2. Customize your message templates
- Message templates are defined as static methods inside:

`automatizacion/templates_messages.py`

`class Templates`

### 3. Run the project
Edit main.py with the path to your Excel file and your desired template.

Example:
```
wpp = MainWorkflow(
    ruta_excel=ruta_excel,
    nombre_asistente="sara",
    nombre_asesor="pablo",
    ruta_carpeta_principal=r"C:\Users\nameUser\Documents"
)

wpp.enviar_mensajes_wpp(Templates.cartera)
```

### 4. Scan the QR code

- When you run the project, a Chrome window will open with WhatsApp Web.

- You must scan the QR code every time for security reasons.
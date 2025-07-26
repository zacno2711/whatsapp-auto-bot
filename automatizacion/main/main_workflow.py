import pandas as pd
from datetime import datetime

from automatizacion.modules.selenium_watsapp import WhatsApp_slm

class MainWorkflow():
    def __init__(self,ruta_excel:str,tipo_plantilla:str,nombre_asistente:str,nombre_asesor:str):
        self.ruta_excel = ruta_excel
        self.tipo_plantilla = tipo_plantilla
        self.nombre_asistente = nombre_asistente
        self.nombre_asesor = nombre_asesor
        self.df_info = pd.read_excel(ruta_excel,dtype=str).fillna("")

    def validar_df_info(self,df:pd.DataFrame) -> pd.DataFrame:
        def validar_columnas(df:pd.DataFrame):
            columnas_necesarias = [
                "Telefono",
                "Nombre Tomador",
                "Ramo",
                "numPoliza",
                "fechaInicioVigencia",
                "fechaFinVigencia"
            ]

            columnas_faltantes = [col for col in columnas_necesarias if col not in df.columns]
            columnas_extras = [col for col in df.columns if col not in columnas_necesarias]

            print("[INFO] Columnas en el DataFrame:", list(df.columns))
            print("[INFO] Columnas necesarias:", columnas_necesarias)

            if columnas_extras:
                print(f"⚠️ [WARNNING] Columnas no requeridas encontradas: {columnas_extras}")

            if columnas_faltantes:
                print(f"❌ [ERROR] Columnas faltantes: {columnas_faltantes}")
                raise ValueError(f"Faltan columnas requeridas: {columnas_faltantes}")

            print("✅ [SUCCSESS] Todas las columnas necesarias están presentes.")

        def validar_fecha(fecha:str):
            if not isinstance(fecha, str):
                raise ValueError(f"El valor '{fecha}' no es un string.")

            if not fecha:
                raise ValueError("La fecha está vacía. Validar contenido.")

            if '/' not in fecha:
                raise ValueError(f"La fecha '{fecha}' no está separada por '/'.")

            try:
                datetime.strptime(fecha, "%Y/%m/%d")
            except ValueError:
                raise ValueError(f"La fecha '{fecha}' no tiene el formato 'YYYY/MM/DD' válido.")

        def validar_ramo(ramo: str):
            if not isinstance(ramo, str):
                raise ValueError(f"El ramo debe ser un string. Se recibió un {type(ramo).__name__}: '{ramo}'")

            if ramo.isdigit():
                return

            if ramo == "BAN":
                return

            raise ValueError(f"El ramo '{ramo}' no es válido. Debe ser un número o 'BAN'.")
        
        def validar_columna_ramo(ramo_str: str):
            if not ramo_str:
                raise ValueError("el ramo esta vacio, revisar")
            if not "-" in ramo_str:
                raise ValueError(f"el ramo '{ramo_str}' no contiene el separador '-', revisar")

        def validar_y_separar_columna(df:pd.DataFrame, columna_original:str, nueva_col1:str, nueva_col2:str, separador="-") -> pd.DataFrame:
            df = df.copy()
            partes_invalidas = df[df[columna_original].str.count(separador) != 1]

            if not partes_invalidas.empty:
                filas_invalidas = partes_invalidas.index.tolist()
                raise ValueError(f"Las siguientes filas no tienen exactamente un separador '{separador}': {filas_invalidas}")

            # Si todas las filas están bien, se hace el split
            df[[nueva_col1, nueva_col2]] = df[columna_original].str.split(separador, expand=True)

            # Eliminar la columna original
            df.drop(columns=[columna_original], inplace=True)
            return df
        
        def validar_numPoliza(numPoliza:str):
            if not isinstance(numPoliza, str):
                raise ValueError(f"El numPoliza debe ser un string. Se recibió un {type(numPoliza).__name__}: '{numPoliza}'")

            if numPoliza.isdigit():
                return

            raise ValueError(f"El numPoliza '{numPoliza}' no es válido. Debe ser un número")
        
        df_info = df.copy()

        validar_columnas(df_info) 
        df_info["Telefono"] = df_info["Telefono"].apply(WhatsApp_slm.validar_y_limpiar_numero_telefono)
        df_info["Ramo"].apply(validar_columna_ramo)
        df_info = validar_y_separar_columna(df_info,"Ramo","codRamo","nomRamo","-")
        df_info["codRamo"].apply(validar_ramo)
        df_info["numPoliza"].apply(validar_numPoliza)

        for col in ["fechaInicioVigencia","fechaFinVigencia"]:
            df_info[col].apply(validar_fecha)

        return df_info

    def enviar_mensajes_wpp(self):
        df_info = self.validar_df_info(self.df_info)
        slm_wpp = WhatsApp_slm()
        slm_wpp.abrir_wpp()

        df_info = df_info.reset_index(drop=True)
        print(f"CANTIDAD DE MENSAJES A ENVIAR = {len(df_info)}")

        for i,info_msg in df_info.iterrows():
            print("=="*5,f"{info_msg["Nombre"]}, {info_msg["numPoliza"]}, {info_msg["Telefono"]} [{i+1}-{len(df_info)}]","=="*5)
            
            mensaje = ""
            
            slm_wpp.enviar_mensaje_wpp(
                numero_telefono = info_msg["Telefono"],
                mensaje=mensaje,
                # ruta_adjunto=ruta_archivo
                )
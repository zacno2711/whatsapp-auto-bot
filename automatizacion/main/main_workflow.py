import os
import pandas as pd
from typing import Callable
from datetime import datetime

from automatizacion.modules.selenium_watsapp import WhatsApp_slm
from librerias.logger_config import get_logger


class MainWorkflow():
    def __init__(self,ruta_excel:str,nombre_asistente:str,nombre_asesor:str,ruta_carpeta_principal:str):
        self.logger = get_logger(self.__class__.__name__)
        self.ruta_excel = ruta_excel
        self.nombre_asistente = nombre_asistente
        self.nombre_asesor = nombre_asesor
        self.df_info = pd.read_excel(ruta_excel,dtype=str).fillna("")
        self.ruta_carpeta_principal = ruta_carpeta_principal

    def validar_df_info(self,df:pd.DataFrame,tipo_template:str) -> pd.DataFrame:
        def validar_columnas(df:pd.DataFrame):
            self.logger.info(f"=== VALIDANDO DF INSUMO PARA TEMPLATE = '{tipo_template}' ===")
            if "cartera" in tipo_template.lower():
                columnas_necesarias = [
                    "Telefono",
                    "nombreTomador",
                    "Ramo",
                    "numPoliza",
                    "dias_mora"
                    # "fechaInicioVigencia",
                    # "fechaFinVigencia"
                ]
            elif "renovacion" in tipo_template.lower():
                columnas_necesarias = [
                    "Telefono",
                    "nombreTomador",
                    "Ramo",
                    "numPoliza",
                    "fechaInicioVigencia",
                    "fechaFinVigencia"
                ]
            else:
                e = f"la plantilla '{tipo_template}' no esta mapeada para validacion"
                self.logger.error(e)
                raise ValueError(e)
            
            columnas_faltantes = [col for col in columnas_necesarias if col not in df.columns]
            columnas_extras = [col for col in df.columns if col not in columnas_necesarias]

            if columnas_extras:
                self.logger.warning(f"Columnas no requeridas encontradas: {columnas_extras}")

            if columnas_faltantes:
                e = f"Columnas faltantes: {columnas_faltantes}"
                self.logger.error(e)
                raise ValueError(e)

        def validar_fecha(fecha:str):
            if not isinstance(fecha, str):
                e = f"El valor '{fecha}' no es un string."
                self.logger.error(e)
                raise ValueError(e)

            if not fecha:
                e = "La fecha está vacía. Validar contenido."
                self.logger.error(e)
                raise ValueError(e)
            
            if '/' not in fecha:
                e = f"La fecha '{fecha}' no está separada por '/'."
                self.logger.error(e)
                raise ValueError(e)

            try:
                datetime.strptime(fecha, "%Y/%m/%d")
            except ValueError:
                e = f"La fecha '{fecha}' no tiene el formato 'YYYY/MM/DD' válido."
                self.logger.error(e)
                raise ValueError(e)

        def validar_ramo(ramo: str):
            if not isinstance(ramo, str):
                e = f"El ramo debe ser un string. Se recibió un {type(ramo).__name__}: '{ramo}'"
                self.logger.error(e)
                raise ValueError(e)

            if ramo.isdigit():
                return

            if ramo == "BAN":
                return

            e = f"El ramo '{ramo}' no es válido. Debe ser un número o 'BAN'."
            self.logger.error(e)
            raise ValueError(e)
        
        def validar_columna_ramo(ramo_str: str):
            if not ramo_str:
                e = "el ramo esta vacio, revisar"
                self.logger.error(e)
                raise ValueError(e)
            if not "-" in ramo_str:
                e = f"el ramo '{ramo_str}' no contiene el separador '-', revisar"
                self.logger.error(e)
                raise ValueError(e)

        def validar_y_separar_columna(df:pd.DataFrame, columna_original:str, nueva_col1:str, nueva_col2:str, separador="-") -> pd.DataFrame:
            df = df.copy()
            partes_invalidas = df[df[columna_original].str.count(separador) != 1]

            if not partes_invalidas.empty:
                filas_invalidas = partes_invalidas.index.tolist()
                e = f"Las siguientes filas no tienen exactamente un separador '{separador}': {filas_invalidas}"
                self.logger.error(e)
                raise ValueError(e)
            
            # Si todas las filas están bien, se hace el split
            df[[nueva_col1, nueva_col2]] = df[columna_original].str.split(separador, expand=True)

            # Eliminar la columna original
            df.drop(columns=[columna_original], inplace=True)
            return df
        
        def validar_numPoliza(numPoliza:str):
            if not isinstance(numPoliza, str):
                e = f"El numPoliza debe ser un string. Se recibió un {type(numPoliza).__name__}: '{numPoliza}'"
                self.logger.error(e)
                raise ValueError(e)


            if numPoliza.isdigit():
                return

            e = f"El numPoliza '{numPoliza}' no es válido. Debe ser un número"
            self.logger.error(e)
            raise ValueError(e)
        
        df_info = df.copy()

        validar_columnas(df_info) 
        self.logger.info("✅ Columnas validadas")
        df_info["Telefono"] = df_info["Telefono"].apply(WhatsApp_slm.validar_y_limpiar_numero_telefono)
        self.logger.info("✅ Teléfonos validados y limpiados")
        df_info["Ramo"].apply(validar_columna_ramo)
        self.logger.info("✅ Columna 'Ramo' validada")
        df_info = validar_y_separar_columna(df_info,"Ramo","codRamo","nomRamo","-")
        self.logger.info("✅ Columna 'Ramo' separada en 'codRamo' y 'nomRamo'")
        df_info["codRamo"].apply(validar_ramo)
        self.logger.info("✅ 'codRamo' validado")
        df_info["numPoliza"].apply(validar_numPoliza)
        self.logger.info("✅ 'numPoliza' validado")

        for col in ["fechaInicioVigencia","fechaFinVigencia"]:
            df_info[col].apply(validar_fecha)
            self.logger.info(f"✅ '{col}' validada")

        return df_info

    def enviar_mensajes_wpp(self,template_mensaje:Callable[[dict | pd.Series], str], probar_plantilla : bool = False):
        nombre_tamplate = template_mensaje.__name__
        
        df_info = self.validar_df_info(
            df = self.df_info,
            tipo_template = nombre_tamplate
            )
        
        df_info = df_info.reset_index(drop=True)
        df_info["nombre_asesor"] = self.nombre_asesor
        df_info["nombre_asistente"] = self.nombre_asistente
        df_info["mensaje"] = df_info.apply(template_mensaje,axis=1)
        
        if probar_plantilla:
            self.logger.info(F"PRUEBA DE PLANTILLA -> '{df_info.iloc[0]["mensaje"]}'")
            return
        
        slm_wpp = WhatsApp_slm()
        slm_wpp.abrir_wpp()

        self.logger.info(f"CANTIDAD DE MENSAJES A ENVIAR = {len(df_info)}")

        try:
            info_result = []
            for i,info_msg in df_info.iterrows():
                self.logger.info(f"{'=='*5} {info_msg['nombreTomador']}, {info_msg['numPoliza']}, {info_msg['Telefono']} [{i+1}-{len(df_info)}] {'=='*5}")
                try:
                    result = slm_wpp.enviar_mensaje_wpp(
                        numero_telefono = info_msg["Telefono"],
                        mensaje = info_msg["mensaje"],
                        # ruta_adjunto=ruta_archivo
                        )
                except Exception as e:
                    e = f"Error al tratar de enviar el mensaje, {e}"
                    self.logger.exception(e)
                    result["result"] = e
                finally:
                    info_result.append(
                        {**info_msg.to_dict(), **result}
                    )
        except:
            raise
        finally:
            self.logger.info("PREPARANDO INFORMACION RESULTADO PARA CREACION DE ARCHIVO")
            if info_result:
                df_result = pd.DataFrame(info_result)
                ruta_carpeta_result = os.path.join(self.ruta_carpeta_principal,self.nombre_asesor.replace(" ","").strip())
                ruta_archivo = os.path.join(ruta_carpeta_result,f'{nombre_tamplate}_{datetime.now().strftime("%d-%m-%Y_%H-%M")}.xlsx')
                if not os.path.exists(ruta_carpeta_result):
                    os.makedirs(ruta_carpeta_result)
                    self.logger.info(f"CARPETA CREADA '{ruta_carpeta_result}'")
                df_result.to_excel(ruta_archivo,index=False)
                self.logger.info(f"✅ ARCHIVO GUARDADO '{ruta_archivo}' CON EXITO")

            else:
                self.logger.error("SIN INFORMACION RESULTADO, NO SE CREARA EL ARCHIVO")
            
import pandas as pd

class Templates :
    @staticmethod
    def cartera(info:dict | pd.Series) -> str:
        # print(info)
        return  f"""
       Buen día *{info["nombreTomador"]}*, espero estés muy bien.
Soy *{info["nombre_asistente"]}*, la asistente de *{info["nombre_asesor"]}* tu asesora de tu seguro SURA 💙, paso por aquí para recordarte el pago de tu seguro de *{info["codRamo"]}* ya que tienes pendiente la vigencia de . Por lo tanto se encuentra en riesgo de cancelación y podría cancelarse sin previo aviso. Ya que tiene *{info["dias_mora"]}* días pendientes por pago. Recuerda que no pagamos mes vencido sino mes anticipado, por lo tanto la fecha que aparece en pago express, es la fecha de pago de tu seguro. Luego de eso es posible que te corten los servicios. Que tengas un feliz día 🌈

*Recuerda que puedes realizar los pagos por pagos.segurossura.com.co/pagos*  
"""

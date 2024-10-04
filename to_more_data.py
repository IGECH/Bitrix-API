import requests
import pandas as pd

# Configuración del Webhook de Bitrix
WEBHOOK_URL = 'https://igech.bitrix24.es/rest/116/5vx5kgyoz64xvky7/'

# Configuración para el pipeline y etapa
PIPELINE_ID = 14  # ID del pipeline
ETAPA_ID = 'C14:NEW'  # ID de la etapa
FILENAME = "negociaciones_enriquecer.csv"  # Nombre del archivo CSV

# Función para obtener las negociaciones de un embudo (pipeline) y una etapa específicos
def obtener_negociaciones(pipeline_id, etapa_id):
    url = f"{WEBHOOK_URL}crm.deal.list"
    
    # Los parámetros deben enviarse como un diccionario en el cuerpo de la solicitud
    params = {
        'filter': {
            'CATEGORY_ID': pipeline_id,  # ID del pipeline (embudo)
            'STAGE_ID': etapa_id  # ID de la etapa
        },
        'select': ['*','UF_CRM_1724766584257', 'UF_CRM_1726250643065', 'UF_CRM_1726258492614', 'UF_CRM_1726599068673', 'UF_CRM_66F2A5356BCEE', 'UF_CRM_1727216328704'], 
        'start': 0  
    }
    
    print(f"Consultando negociaciones con pipeline ID: {pipeline_id} y etapa ID: {etapa_id}")
   
    response = requests.post(url, json=params)  # Usamos POST y enviamos los parámetros como JSON
    response.raise_for_status()  # Manejo de errores HTTP
    
    data = response.json()
    
    if 'result' in data:
        return data['result']
    else:
        return []  # Si no hay negociaciones, devolvemos una lista vacía

# Guardar negociaciones en un archivo CSV en formato UTF-8 con separador ;
def guardar_negociaciones_csv(negociaciones, filename):
    if negociaciones:
        df = pd.DataFrame(negociaciones)
        # Guardar como CSV con codificación UTF-8 y separador ;
        df.to_csv(filename, index=False, sep=';', encoding='utf-8-sig')  
        print(f"Negociaciones exportadas a {filename}")
    else:
        print("No se encontraron negociaciones para exportar.")

# Ejecutar la obtención de negociaciones y guardarlas en un archivo CSV
negociaciones = obtener_negociaciones(PIPELINE_ID, ETAPA_ID)
guardar_negociaciones_csv(negociaciones, FILENAME)

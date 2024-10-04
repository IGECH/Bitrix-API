import requests

WEBHOOK_URL = 'https://igech.bitrix24.es/rest/116/5vx5kgyoz64xvky7/'

def obtener_embudos():
    url = f"{WEBHOOK_URL}crm.dealcategory.list"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    embudos = data['result']

    # Agregar el embudo por defecto (ID 0) manualmente
    embudo_por_defecto = {
        'ID': 0,
        'NAME': 'Desarrollo'
    }
    embudos.insert(0, embudo_por_defecto)  # Insertar el embudo por defecto al principio
    return embudos

# Mostrar los embudos disponibles, incluyendo el embudo por defecto
embudos = obtener_embudos()

def obtener_etapas(embudo_id):
    url = f"{WEBHOOK_URL}crm.dealcategory.stage.list"
    params = {"id": embudo_id}  
    print(f"Consultando las etapas para el embudo {embudo_id} con la URL: {url} y los parámetros: {params}")
    
    response = requests.get(url, params=params)
    response.raise_for_status()  # Manejo de errores HTTP
    data = response.json()
    return data['result']

# Iterar sobre los embudos para obtener y mostrar sus etapas
for embudo in embudos:
    etapas = obtener_etapas(embudo["ID"])  
    print(f"PIPELINE: {embudo['ID']} {embudo['NAME'].upper()}")
    for etapa in etapas:
        print(f"ID de la etapa: {etapa['STATUS_ID']}, Nombre: {etapa['NAME']}")

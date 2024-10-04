import requests

# Configuración del Webhook de Bitrix
BITRIX_WEBHOOK = "https://igech.bitrix24.es/rest/116/5vx5kgyoz64xvky7/"

# Función para obtener los campos de negociación, incluidos los personalizados
def obtener_campos_negociacion():
    url = f"{BITRIX_WEBHOOK}crm.deal.fields"
    response = requests.get(url)
    response.raise_for_status()  # Verificar si la solicitud fue exitosa
    data = response.json()

    # Filtrar campos personalizados por el prefijo 'UF_CRM_'
    campos_personalizados = {k: v for k, v in data['result'].items() if k.startswith('UF_CRM_')}
    
    return campos_personalizados

# Obtener y mostrar los campos personalizados
campos_personalizados = obtener_campos_negociacion()
for campo, info in campos_personalizados.items():
    # print(info)
    if info['items']:
        print(f"ID del campo: {campo}, Nombre: {info['listLabel']}, OPCIONES: {info['items']}")
    else:
        print(f"ID del campo: {campo}, Nombre: {info['listLabel']}")

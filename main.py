import requests
import pandas as pd

# Reemplaza con tu webhook de Bitrix24
WEBHOOK_URL = "https://igech.bitrix24.es/rest/116/3q3ung204hft1qqiq82myq3rh9fow6tt/"

# Función para obtener las negociaciones de una etapa específica
def obtener_negociaciones(embudo_id, etapa_id):
    url = f"{WEBHOOK_URL}crm.deal.list"
    params = {
        "filter": {
            "STAGE_ID": etapa_id,
            "CATEGORY_ID": embudo_id
        },
        "select": ["ID", "TITLE", "CONTACT_ID", "COMPANY_ID", "OPPORTUNITY"]
    }
    response = requests.get(url, params=params)
    response.raise_for_status()  # Manejo de errores HTTP
    data = response.json()
    return data.get('result', [])

# Función para obtener datos del cliente
def obtener_contacto(contact_id):
    url = f"{WEBHOOK_URL}crm.contact.get"
    params = {"id": contact_id}
    response = requests.get(url, params=params)
    response.raise_for_status()  # Manejo de errores HTTP
    return response.json()

# Exportar los datos a Excel
def exportar_a_excel(datos):
    df = pd.DataFrame(datos)
    df.to_excel("negociaciones_exportadas.xlsx", index=False)

if __name__ == "__main__":
    # Reemplaza con el ID de tu embudo y etapa
    embudo_id = 14  # Ejemplo de embudo
    etapa_id = "Enriquecimiento de datos"  # Etapa específica

    # Obtener las negociaciones de la etapa
    negociaciones = obtener_negociaciones(embudo_id, etapa_id)

    # Crear una lista con los datos a exportar
    lista_exportacion = []
    for negociacion in negociaciones:
        contact_id = negociacion.get('CONTACT_ID')
        if contact_id:
            contacto = obtener_contacto(contact_id)
            negociacion['CONTACT_NAME'] = contacto.get('result', {}).get('NAME', 'No disponible')
        lista_exportacion.append(negociacion)

    # Exportar los datos a un archivo Excel
    exportar_a_excel(lista_exportacion)
    print("Exportación completada.")


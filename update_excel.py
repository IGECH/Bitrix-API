import requests
import pandas as pd

# Configuración del Webhook de Bitrix
BITRIX_WEBHOOK = "https://igech.bitrix24.es/rest/116/5vx5kgyoz64xvky7/"

# Archivos CSV: ahora trabajamos con archivos CSV en lugar de Excel
OLD_FILE = "negociaciones_enriquecer.csv"  # Archivo original (UTF-8 y separado por ;)
ENRICHED_FILE = "enriquecido.csv"  # Archivo enriquecido (UTF-8 y separado por ;)

# Función para actualizar una negociación en Bitrix
def update_negotiation(deal_id, updated_fields):
    url = f"{BITRIX_WEBHOOK}crm.deal.update"
    
    # Eliminar valores NaN o reemplazarlos con None
    updated_fields_clean = {k: (v if pd.notna(v) else None) for k, v in updated_fields.items()}
    
    params = {
        'ID': deal_id,
        'fields': updated_fields_clean
    }
    
    response = requests.post(url, json=params).json()
    return response

# Función para comparar archivos y generar actualizaciones
def compare_and_update():
    # Cargar ambos archivos CSV
    old_df = pd.read_csv(OLD_FILE, sep=';', encoding='utf-8-sig')  # Archivo original
    enriched_df = pd.read_csv(ENRICHED_FILE, sep=';', encoding='utf-8-sig')  # Archivo enriquecido

    # Iterar sobre las negociaciones enriquecidas
    for index, enriched_row in enriched_df.iterrows():
        deal_id = enriched_row['ID']
        old_row = old_df[old_df['ID'] == deal_id].iloc[0]

        # Encontrar los campos que han cambiado
        updates = {}
        for column in enriched_df.columns:
            if enriched_row[column] != old_row[column]:
                updates[column] = enriched_row[column]
        
        # Si hay cambios, actualizar la negociación en Bitrix
        if updates:
            response = update_negotiation(deal_id, updates)
            if 'error' not in response:
                print(f"Negociación {deal_id} actualizada con éxito.")
            else:
                print(f"Error al actualizar la negociación {deal_id}: {response['error_description']}")

# Ejecutar comparación y actualización
compare_and_update()

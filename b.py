import requests

# Tu clave API de COSMIC (deberías sustituir 'tu_clave_api' por tu clave)
api_key = 'tu_clave_api'

# El gen que queremos consultar, por ejemplo, TP53
gene = 'TP53'

# URL de la API de COSMIC
url = f'https://cancer.sanger.ac.uk/cosmic/api/v1/gene/{gene}/mutations'

# Configurar los parámetros de la solicitud
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# Hacer la solicitud GET a la API
response = requests.get(url, headers=headers)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Obtener los datos de las mutaciones
    mutation_data = response.json()

    # Imprimir los primeros resultados de las mutaciones
    print(mutation_data)
else:
    print(f'Error al obtener los datos: {response.status_code}')
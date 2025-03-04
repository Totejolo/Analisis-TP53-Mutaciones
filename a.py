import requests
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from io import StringIO

# Función para obtener los datos de STRING
def get_ppu_data(query_protein):
    url = f"https://string-db.org/api/tsv/network?identifiers={query_protein}&species=9606"  # 9606 es el ID para Homo sapiens (humano)
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

# Obtener los datos para la proteína 'TP53'
protein = 'TP53'
ppi_data = get_ppu_data(protein)

# Mostrar las primeras líneas de los datos obtenidos para ver la estructura
if ppi_data:
    # Convertir los datos en un DataFrame para ver las columnas
    data = StringIO(ppi_data)
    df = pd.read_csv(data, sep='\t')
    
    # Limpiar los nombres de las columnas para eliminar espacios adicionales o caracteres invisibles
    df.columns = df.columns.str.strip()

    # Imprimir las columnas para asegurarnos de la correcta estructura
    print("Nombres de las columnas:")
    print(df.columns.tolist())  # Asegura que vemos todas las columnas
    
    # Verificar las primeras filas del DataFrame
    print("\nPrimeras filas del DataFrame:")
    print(df.head())  # Muestra las primeras filas para ver los datos y las columnas
else:
    print("Error al obtener datos.")

# Función para procesar los datos y crear un grafo
def create_network_from_ppi_data(ppi_data):
    # Convertir los datos en un DataFrame de pandas
    data = StringIO(ppi_data)
    df = pd.read_csv(data, sep='\t')

    # Limpiar los nombres de las columnas para eliminar espacios adicionales
    df.columns = df.columns.str.strip()

    # Crear un grafo vacío
    G = nx.Graph()
    
    # Añadir nodos y aristas al grafo a partir de los datos de interacción
    for index, row in df.iterrows():
        # Usar las columnas correctas
        protein1 = row['preferredName_A']  # Ahora usamos 'preferredName_A'
        protein2 = row['preferredName_B']  # Ahora usamos 'preferredName_B'
        score = row['score']  # La columna 'score' sigue siendo correcta
        
        # Añadir una arista entre las dos proteínas
        G.add_edge(protein1, protein2, weight=score)
    
    return G

# Crear la red de interacciones
if ppi_data:
    G = create_network_from_ppi_data(ppi_data)
    print(f"Red creada con {len(G.nodes)} nodos y {len(G.edges)} aristas.")
else:
    print("No se pudo crear la red.")

# Visualización de la red de interacción
def visualize_network(G):
    plt.figure(figsize=(12, 12))
    
    # Dibujar la red
    pos = nx.spring_layout(G, k=0.15, iterations=20)  # El layout define cómo se organiza el grafo
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color='blue', alpha=0.6)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
    
    plt.title("Red de Interacción Proteína-Proteína")
    plt.axis('off')
    plt.show()

# Visualizar el grafo
if ppi_data:
    visualize_network(G)
import matplotlib.pyplot as plt
import networkx as nx

# Visualización mejorada del grafo
def visualize_network(G):
    plt.figure(figsize=(12, 12))
    
    # Layout para una distribución más estética
    pos = nx.spring_layout(G, k=0.15, iterations=20)  # Se puede cambiar a otro layout
    
    # Obtener los grados de los nodos (cantidad de interacciones)
    degrees = dict(G.degree())
    
    # Colorear los nodos según el grado
    node_color = [degrees[node] for node in G.nodes]
    
    # Definir el tamaño de los nodos en función de su grado
    node_size = [degrees[node] * 100 for node in G.nodes]  # Ajustar multiplicador para hacer los nodos más grandes
    
    # Dibujar los nodos, aristas y etiquetas
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.viridis, alpha=0.7)
    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')
    
    # Añadir un título y leyenda
    plt.title("Red de Interacción Proteína-Proteína", fontsize=15)
    plt.axis('off')
    
    # Mostrar el gráfico
    plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.viridis), label="Grado de nodo")  # Colorbar para grados
    plt.show()

# Llamar a la función para visualizar el grafo
visualize_network(G)
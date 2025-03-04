import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

# Cargar el archivo CSV limpio
df = pd.read_csv('archivo_convertido.csv')

# Verificar nombres de columnas y eliminar espacios extra
df.columns = df.columns.str.strip()

# Mostrar las columnas disponibles para verificar si "Position" existe
print("Columnas en el archivo CSV:", df.columns.tolist())

# Seleccionar columnas relevantes, excluyendo "Position" si no existe
cols_interes = ['Gene(s)', 'Protein change', 'Molecular consequence', 'Oncogenicity classification']
df_cleaned = df[cols_interes].dropna()

# Contar mutaciones por gen
gene_counts = df_cleaned['Gene(s)'].value_counts()
print("Cantidad de mutaciones por gen:")
print(gene_counts)

# Gráfico 1: Distribución de mutaciones en TP53 (solo si 'Position' está disponible)
if 'Position' in df.columns:
    plt.figure(figsize=(12, 6))
    sns.histplot(df['Position'], bins=30, kde=True, color='purple')
    plt.xlabel('Posición en la Secuencia de TP53')
    plt.ylabel('Frecuencia de Mutaciones')
    plt.title('Distribución de Mutaciones en el Gen TP53')
    plt.show()
else:
    print("No se encontró una columna de posición de mutación en el archivo.")

# Gráfico 2: Mutaciones por gen (Top 10)
top_genes = gene_counts.head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_genes.index, y=top_genes.values, palette='viridis')
plt.xlabel('Gen')
plt.ylabel('Número de Mutaciones')
plt.title('Número de Mutaciones por Gen')
plt.xticks(rotation=45)
plt.show()

# Cargar los datos de interacciones de proteínas con el separador corregido
archivo_interacciones = "9606.protein.physical.links.detailed.v12.0.txt.gz"
df_interacciones = pd.read_csv(archivo_interacciones, sep=r"\s+", header=None, low_memory=False)

# Asignar nombres a las columnas según la estructura del archivo
df_interacciones.columns = ["Protein1", "Protein2", "Experimental", "Database", "TextMining", "CombinedScore"]

# Ver primeras filas para revisar que los datos estén correctos
print(df_interacciones.head())

# Convertir 'CombinedScore' a numérico y eliminar valores NaN
df_interacciones['CombinedScore'] = pd.to_numeric(df_interacciones['CombinedScore'], errors='coerce')
df_interacciones = df_interacciones.dropna(subset=['CombinedScore'])

# Filtrar interacciones con CombinedScore > 500
df_interacciones_filtered = df_interacciones[df_interacciones['CombinedScore'] > 500]

# Crear el grafo con NetworkX
G_filtered = nx.Graph()
for _, row in df_interacciones_filtered.iterrows():
    G_filtered.add_edge(row['Protein1'], row['Protein2'], weight=row['CombinedScore'])

# Exportar el grafo a un archivo GML para Gephi
nx.write_gml(G_filtered, "interacciones_proteinas.gml")
print("\nGrafo exportado correctamente a 'interacciones_proteinas.gml'.")
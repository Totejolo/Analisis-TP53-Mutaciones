import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

# Cargar el archivo CSV limpio
df = pd.read_csv('archivo_convertido.csv')

# Verificar nombres de columnas y eliminar espacios extra
df.columns = df.columns.str.strip()

# Seleccionar columnas relevantes
cols_interes = ['Gene(s)', 'Protein change', 'Molecular consequence', 'Oncogenicity classification']
df_cleaned = df[cols_interes]

# Contar mutaciones por gen
gene_counts = df_cleaned['Gene(s)'].value_counts()
print("Cantidad de mutaciones por gen:")
print(gene_counts)

# Gráfico de barras de mutaciones por gen (solo los 10 primeros genes más mutados)
top_genes = gene_counts.head(10)  # Mostrar los 10 genes más frecuentes
plt.figure(figsize=(10, 6))
sns.barplot(x=top_genes.index, y=top_genes.values, palette='viridis')
plt.xlabel('Gen')
plt.ylabel('Número de Mutaciones')
plt.title('Número de Mutaciones por Gen')
plt.xticks(rotation=45)
plt.show()

# Contar clasificaciones oncogénicas
oncogenic_counts = df_cleaned['Oncogenicity classification'].value_counts()
print("\nDistribución de la clasificación oncogénica:")
print(oncogenic_counts)

# Gráfico de pastel de clasificación oncogénica
plt.figure(figsize=(8, 8))
plt.pie(oncogenic_counts, labels=oncogenic_counts.index, autopct='%1.1f%%', colors=['#ff9999','#66b3ff'])
plt.title('Distribución de la Clasificación Oncogénica')
plt.show()

# Análisis de consecuencias moleculares
consequence_counts = df_cleaned['Molecular consequence'].value_counts()
print("\nTipos de consecuencias moleculares:")
print(consequence_counts)

# Gráfico de barras de consecuencias moleculares (sin 'hue' ya que no es necesario)
plt.figure(figsize=(12, 6))
sns.barplot(y=consequence_counts.index, x=consequence_counts.values, palette='coolwarm')
plt.xlabel('Frecuencia')
plt.ylabel('Tipo de Consecuencia Molecular')
plt.title('Frecuencia de Consecuencias Moleculares')
plt.show()

# Guardar resultados en un nuevo CSV
df_cleaned.to_csv('archivo_analizado.csv', index=False)
print("\nAnálisis completado y guardado en 'archivo_analizado.csv'.")

# Cargar los datos de interacciones de proteínas
archivo_interacciones = "9606.protein.physical.links.detailed.v12.0.txt.gz"  # Asegúrate de tener la ruta correcta

# Leer el archivo de interacciones (utilizamos \s+ para separar por espacios múltiples)
df_interacciones = pd.read_csv(archivo_interacciones, sep="\s+", header=None, low_memory=False)

# Ajustar las columnas según lo que hemos visto en el archivo
df_interacciones.columns = ["Protein1", "Protein2", "Experimental", "Database", "TextMining", "CombinedScore"]

# Mostrar las primeras filas para revisar las columnas
print(df_interacciones.head())

# Asegurarnos de que la columna 'CombinedScore' sea numérica y eliminar filas con valores no numéricos
df_interacciones['CombinedScore'] = pd.to_numeric(df_interacciones['CombinedScore'], errors='coerce')

# Eliminar las filas con valores NaN en 'CombinedScore'
df_interacciones = df_interacciones.dropna(subset=['CombinedScore'])

# Filtrar interacciones con un CombinedScore alto (mayor a 500)
df_interacciones_filtered = df_interacciones[df_interacciones['CombinedScore'] > 500]  # Ajusta el umbral

# Crear el grafo con las interacciones filtradas
G_filtered = nx.Graph()

# Añadir las interacciones al grafo con el peso como 'CombinedScore'
for _, row in df_interacciones_filtered.iterrows():
    G_filtered.add_edge(row['Protein1'], row['Protein2'], weight=row['CombinedScore'])

# Exportar el grafo a un archivo GML para Gephi
nx.write_gml(G_filtered, "interacciones_proteinas.gml")

print("\nGrafo exportado correctamente a 'interacciones_proteinas.gml'.")


# TP53 mutations and the protein-protein interaction network

Code for the preprint *Analysis of Mutations in TP53 and Its Protein-Protein Interaction Network: Implications in Oncogenesis* (https://doi.org/10.6084/m9.figshare.28704893).

Two strands of analysis: the interaction network around TP53, and the distribution of reported mutations and their oncogenicity classification.

## Scripts

**`a.py` — interaction network.** Queries the STRING API for TP53 in *Homo sapiens* (taxon 9606), builds an undirected graph with networkx using the interaction score as edge weight, and draws it with node size and colour scaled by node degree.

**`b.py` — COSMIC query.** Template for querying the COSMIC mutation API. Note that the `api_key` variable is a placeholder, so this script needs your own COSMIC credentials before it will run.

**`c.py` and `d.py` — mutation distribution.** Read `archivo_convertido.csv` and summarise mutations by gene, molecular consequence and oncogenicity classification, plotting the ten most frequently mutated genes. `d.py` is the fuller version: it drops incomplete rows and adds a positional histogram when a Position column is available.

## Files

| File | What it is |
|---|---|
| `clinvar_result.txt` | Raw export from ClinVar |
| `archivo_convertido.csv` | The export converted to CSV — input for c.py and d.py |
| `archivo_limpio.csv`, `archivo_analizado.csv` | Intermediate cleaned and analysed tables |
| `mutaciones_oncogenicas.csv` | Variants classified as oncogenic |
| `interacciones_proteinas.gml` | The STRING network exported as GML |
| `ada.gephi`, `ada1.gephi` | Gephi projects for network visualisation |

## Requirements

Python 3.9+

```
pip install pandas matplotlib seaborn networkx requests
```

## Data sources

ClinVar for the variant records and STRING for the interaction network. Both public; no patient data is used.
# TP53_Mutations_Oncogenesis
Analysis of mutations in the TP53 gene and their impact on the protein-protein interaction network in oncogenesis.

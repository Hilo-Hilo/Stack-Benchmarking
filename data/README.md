# Data Directory

This directory contains the datasets for Stack benchmarking experiments.

## Structure

```
data/
├── raw/           # Original, unmodified datasets
│   └── *.h5ad    # Single-cell expression data
│   └── *.csv     # Drug response data
├── processed/    # Processed/transformed data
│   └── *.pkl     # Gene lists, preprocessed features
└── README.md
```

## Required Data Files

### Raw Data

1. **Single-cell expression** (`raw/*.h5ad`)
   - Format: AnnData (HDF5)
   - Required columns: gene expression matrix
   - Gene names must use HGNC symbols (to match Stack vocabulary)
   - Example: 15,012 genes from Stack's training vocabulary

2. **Drug response** (`raw/*response*.csv`)
   - Format: CSV with columns
     - `drug_id`: Drug identifier
     - `cell_line_id`: Cell line identifier  
     - `AUC`: Area Under Curve (response metric)
     - `IC50`: Half-maximal inhibitory concentration
     - `tissue`: Tissue of origin

### Processed Data

- `processed/genelist.pkl`: Selected gene list for modeling
- `processed/*.npy`: Precomputed embeddings

## Generating Synthetic Data

For testing, generate synthetic data:

```bash
python src/data/generate_synthetic.py
```

This creates:
- `synthetic_base.h5ad` - Control/ untreated cells
- `synthetic_perturbation.h5ad` - Treated cells  
- `synthetic_drug_response.csv` - Response values

Note: Synthetic data uses placeholder gene names (gene_0, gene_1, etc.) and will NOT work with Stack embeddings. Use real data with HGNC gene symbols.
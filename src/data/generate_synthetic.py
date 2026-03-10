"""
Generate synthetic single-cell perturbation data for testing the Stack benchmarking pipeline.
"""
import numpy as np
import pandas as pd
import scanpy as sc
from pathlib import Path


def generate_synthetic_perturbation_data(
    n_cell_lines: int = 50,
    n_drugs: int = 20,
    n_genes: int = 2000,
    n_cells_per_line: int = 100,
    output_dir: str = "data/raw"
) -> dict:
    """
    Generate synthetic single-cell perturbation dataset.
    
    Returns dict with:
    - base_data: AnnData of untreated cells
    - perturbation_data: AnnData of treated cells  
    - drug_response: DataFrame with AUC values
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    np.random.seed(42)
    
    genes = [f"gene_{i}" for i in range(n_genes)]
    cell_lines = [f"CL_{i:03d}" for i in range(n_cell_lines)]
    drugs = [f"drug_{i:02d}" for i in range(n_drugs)]
    
    print(f"Generating {n_cell_lines} cell lines x {n_drugs} drugs x {n_cells_per_line} cells...")
    
    # Generate base (untreated) expression profiles
    # Each cell line has a baseline expression signature
    cell_line_effects = np.random.randn(n_cell_lines, n_genes) * 2 + 10
    
    all_obs = []
    all_X = []
    
    for cl_idx, cl in enumerate(cell_lines):
        for drug_idx, drug in enumerate(drugs):
            for cell_idx in range(n_cells_per_line):
                # Base expression + cell line effect + noise
                base_expr = cell_line_effects[cl_idx]
                noise = np.random.randn(n_genes) * 0.5
                
                # Drug effect (some drugs affect specific gene modules)
                drug_effect = np.zeros(n_genes)
                # Create synthetic drug mechanisms
                affected_genes = np.random.choice(n_genes, size=n_genes//10, replace=False)
                drug_effect[affected_genes] = np.random.randn(len(affected_genes)) * 1.5
                
                expr = base_expr + noise + drug_effect
                
                all_obs.append({
                    "cell_id": f"{cl}_{drug}_{cell_idx}",
                    "cell_line_id": cl,
                    "drug_id": drug,
                    "condition": "treated",
                    "donor_id": cl
                })
                all_X.append(expr)
    
    X = np.array(all_X)
    obs = pd.DataFrame(all_obs)
    
    # Create AnnData
    adata = sc.AnnData(X=X)
    adata.obs_names = obs["cell_id"]
    adata.var_names = genes
    adata.obs = obs
    
    # Save as h5ad
    output_path = output_dir / "synthetic_perturbation.h5ad"
    adata.write_h5ad(output_path)
    print(f"Saved to {output_path}")
    
    # Generate drug response summary (AUC values)
    # Simulate realistic AUC values (0-1, skewed towards higher = more resistant)
    auc_values = np.random.beta(2, 2, size=(n_cell_lines, n_drugs))
    
    drug_response = []
    for cl_idx, cl in enumerate(cell_lines):
        for drug_idx, drug in enumerate(drugs):
            drug_response.append({
                "cell_line_id": cl,
                "drug_id": drug,
                "AUC": auc_values[cl_idx, drug_idx],
                "IC50": -np.log10(auc_values[cl_idx, drug_idx] + 0.01),
                "tissue": np.random.choice(["lung", "breast", "colon", "ovarian"])
            })
    
    response_df = pd.DataFrame(drug_response)
    response_path = output_dir / "synthetic_drug_response.csv"
    response_df.to_csv(response_path, index=False)
    print(f"Saved to {response_path}")
    
    # Also save just untreated cells as "base" for Stack generation
    base_obs = []
    base_X = []
    for cl_idx, cl in enumerate(cell_lines):
        for cell_idx in range(n_cells_per_line):
            base_expr = cell_line_effects[cl_idx] + np.random.randn(n_genes) * 0.3
            base_obs.append({
                "cell_id": f"{cl}_base_{cell_idx}",
                "cell_line_id": cl,
                "condition": "control",
                "donor_id": cl
            })
            base_X.append(base_expr)
    
    base_adata = sc.AnnData(X=np.array(base_X))
    base_adata.obs_names = [o["cell_id"] for o in base_obs]
    base_adata.var_names = genes
    base_adata.obs = pd.DataFrame(base_obs)
    
    base_path = output_dir / "synthetic_base.h5ad"
    base_adata.write_h5ad(base_path)
    print(f"Saved to {base_path}")
    
    return {
        "perturbation": adata,
        "base": base_adata,
        "drug_response": response_df
    }


if __name__ == "__main__":
    generate_synthetic_perturbation_data(
        n_cell_lines=50,
        n_drugs=20,
        n_genes=2000,
        n_cells_per_line=50,
        output_dir="data/raw"
    )

"""
Stack perturbation prediction wrapper for Stack-Benchmarking.
"""
import os
import subprocess
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd
import scanpy as sc


class StackRunner:
    """Wrapper for Stack CLI tools."""
    
    def __init__(
        self,
        stack_repo: str = "~/stack",
        checkpoint: str = "pretrained",
        output_dir: str = "outputs"
    ):
        self.stack_repo = Path(stack_repo).expanduser()
        self.checkpoint = checkpoint
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Add stack CLI to PATH
        self.cli_path = self.stack_repo / "src" / "stack" / "cli"
        
    def embed(
        self,
        adata_path: str,
        genelist_path: str,
        output_path: str,
        batch_size: int = 32
    ):
        """Embed single-cell data using Stack."""
        cmd = [
            "python", "-m", "stack.cli.embedding",
            "--checkpoint", self.checkpoint,
            "--adata", adata_path,
            "--genelist", genelist_path,
            "--output", output_path,
            "--batch-size", str(batch_size)
        ]
        result = subprocess.run(cmd, cwd=self.stack_repo, capture_output=True, text=True)
        return result
    
    def generate(
        self,
        base_adata: str,
        test_adata: str,
        genelist_path: str,
        output_dir: str,
        split_column: str = "donor_id"
    ):
        """Generate perturbation predictions using Stack."""
        cmd = [
            "python", "-m", "stack.cli.generation",
            "--checkpoint", self.checkpoint,
            "--base-adata", base_adata,
            "--test-adata", test_adata,
            "--genelist", genelist_path,
            "--output-dir", output_dir,
            "--split-column", split_column
        ]
        result = subprocess.run(cmd, cwd=self.stack_repo, capture_output=True, text=True)
        return result
    
    def compute_hvg(
        self,
        data_paths: list,
        n_top_genes: int = 1000,
        output_path: str = "hvg.pkl"
    ):
        """Compute highly variable genes across datasets."""
        from stack.data.datasets import compute_hvg_union, DatasetConfig
        
        configs = [DatasetConfig(path=p, filter_organism=True) for p in data_paths]
        hvg_genes = compute_hvg_union(configs, n_top_genes=n_top_genes, output_path=output_path)
        return hvg_genes


def load_ccle_data(data_dir: str = "data/raw") -> sc.AnnData:
    """Load and preprocess CCLE expression data."""
    data_dir = Path(data_dir)
    
    # Look for CCLE data files
    ccle_files = list(data_dir.glob("CCLE*.csv")) + list(data_dir.glob("ccle*.csv"))
    
    if not ccle_files:
        raise FileNotFoundError(f"No CCLE data found in {data_dir}")
    
    # Load expression matrix
    expr_file = [f for f in ccle_files if "expression" in f.name.lower() or "gene" in f.name.lower()]
    if expr_file:
        expr = pd.read_csv(expr_file[0], index_col=0)
        adata = sc.AnnData(X=expr.values.T)
        adata.obs_names = expr.columns
        adata.var_names = expr.index
    else:
        # Generic load
        expr = pd.read_csv(ccle_files[0], index_col=0)
        adata = sc.AnnData(X=expr.values)
        adata.obs_names = expr.index
        adata.var_names = expr.columns
    
    # Basic preprocessing
    sc.pp.filter_genes(adata, min_cells=10)
    sc.pp.filter_cells(adata, min_genes=200)
    
    return adata


def load_drug_response(data_dir: str = "data/raw") -> pd.DataFrame:
    """Load drug response data (AUC, IC50, etc.)."""
    data_dir = Path(data_dir)
    
    # Look for drug response files
    drug_files = list(data_dir.glob("*response*.csv")) + \
                 list(data_dir.glob("*AUC*.csv")) + \
                 list(data_dir.glob("*sensitivity*.csv"))
    
    if not drug_files:
        raise FileNotFoundError(f"No drug response data found in {data_dir}")
    
    return pd.read_csv(drug_files[0], index_col=0)


if __name__ == "__main__":
    # Quick test
    runner = StackRunner()
    print(f"Stack repo: {runner.stack_repo}")
    print(f"Output dir: {runner.output_dir}")

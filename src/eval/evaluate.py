"""
Evaluation pipeline for OOD drug response prediction.
"""
from dataclasses import dataclass
from typing import Optional
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, r2_score, mean_squared_error


@dataclass
class EvaluationResults:
    """Container for evaluation results."""
    metric: str
    value: float
    std: Optional[float] = None
    n_samples: int = 0
    split_type: str = ""


class OODEvaluator:
    """
    Out-of-distribution evaluation for drug response prediction.
    
    Implements:
    - Random splits
    - Cold-drug splits (drugs in test not seen in train)
    - Cold-cell splits (cell lines in test not seen in train)
    """
    
    def __init__(self, drug_response: pd.DataFrame):
        self.drug_response = drug_response
        
    def random_split(
        self, 
        test_fraction: float = 0.2, 
        seed: int = 42
    ) -> tuple:
        """Random train/test split."""
        np.random.seed(seed)
        n = len(self.drug_response)
        test_mask = np.random.rand(n) < test_fraction
        
        train = self.drug_response[~test_mask]
        test = self.drug_response[test_mask]
        
        return train, test
    
    def cold_drug_split(
        self, 
        test_fraction: float = 0.2, 
        seed: int = 42
    ) -> tuple:
        """Hold out entire drugs for testing."""
        np.random.seed(seed)
        
        drugs = self.drug_response["drug_id"].unique()
        n_test_drugs = int(len(drugs) * test_fraction)
        
        test_drugs = np.random.choice(drugs, n_test_drugs, replace=False)
        
        train = self.drug_response[~self.drug_response["drug_id"].isin(test_drugs)]
        test = self.drug_response[self.drug_response["drug_id"].isin(test_drugs)]
        
        return train, test
    
    def cold_cell_split(
        self, 
        test_fraction: float = 0.2, 
        seed: int = 42
    ) -> tuple:
        """Hold out entire cell lines for testing."""
        np.random.seed(seed)
        
        cells = self.drug_response["cell_line_id"].unique()
        n_test_cells = int(len(cells) * test_fraction)
        
        test_cells = np.random.choice(cells, n_test_cells, replace=False)
        
        train = self.drug_response[~self.drug_response["cell_line_id"].isin(test_cells)]
        test = self.drug_response[self.drug_response["cell_line_id"].isin(test_cells)]
        
        return train, test
    
    def tissue_aware_split(
        self,
        test_tissue: str,
        seed: int = 42
    ) -> tuple:
        """Hold out specific tissue type for testing."""
        np.random.seed(seed)
        
        train = self.drug_response[self.drug_response["tissue"] != test_tissue]
        test = self.drug_response[self.drug_response["tissue"] == test_tissue]
        
        return train, test


def compute_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    task_type: str = "regression"
) -> dict:
    """Compute evaluation metrics."""
    
    results = {}
    
    if task_type == "regression":
        results["r2"] = r2_score(y_true, y_pred)
        results["mse"] = mean_squared_error(y_true, y_pred)
        results["rmse"] = np.sqrt(results["mse"])
        results["pearson"] = np.corrcoef(y_true, y_pred)[0, 1]
    elif task_type == "classification":
        # Binary classification (sensitive vs resistant)
        results["auc"] = roc_auc_score(y_true, y_pred)
        results["accuracy"] = np.mean((y_pred > 0.5) == y_true)
    
    return results


def aggregate_by_drug(
    metrics_df: pd.DataFrame,
    agg_func: str = "mean"
) -> pd.DataFrame:
    """Aggregate metrics at drug level."""
    
    if agg_func == "mean":
        return metrics_df.groupby("drug_id").mean()
    elif agg_func == "median":
        return metrics_df.groupby("drug_id").median()
    else:
        raise ValueError(f"Unknown aggregation: {agg_func}")


def aggregate_by_cell(
    metrics_df: pd.DataFrame,
    agg_func: str = "mean"
) -> pd.DataFrame:
    """Aggregate metrics at cell line level."""
    
    if agg_func == "mean":
        return metrics_df.groupby("cell_line_id").mean()
    elif agg_func == "median":
        return metrics_df.groupby("cell_line_id").median()
    else:
        raise ValueError(f"Unknown aggregation: {agg_func}")


def compute_aac(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Compute Area Above the Curve (AAC).
    AAC = 1 - AUC, useful when lower response = better (IC50).
    """
    auc = roc_auc_score(y_true, y_pred)
    return 1 - auc


def report_results(
    results: dict,
    split_type: str,
    drug_level: Optional[pd.DataFrame] = None,
    cell_level: Optional[pd.DataFrame] = None
) -> str:
    """Generate human-readable results report."""
    
    report = f"\n{'='*50}\n"
    report += f"Results: {split_type} split\n"
    report += f"{'='*50}\n"
    
    for metric, value in results.items():
        if isinstance(value, float):
            report += f"{metric:20s}: {value:.4f}\n"
        else:
            report += f"{metric:20s}: {value}\n"
    
    if drug_level is not None:
        report += f"\n--- Per-Drug Summary ---\n"
        report += f"Mean R2: {drug_level['r2'].mean():.4f}\n"
        report += f"Median R2: {drug_level['r2'].median():.4f}\n"
    
    if cell_level is not None:
        report += f"\n--- Per-Cell-Line Summary ---\n"
        report += f"Mean R2: {cell_level['r2'].mean():.4f}\n"
        report += f"Median R2: {cell_level['r2'].median():.4f}\n"
    
    return report


if __name__ == "__main__":
    # Quick test
    np.random.seed(42)
    n = 1000
    
    # Dummy drug response data
    drug_response = pd.DataFrame({
        "drug_id": np.random.choice(["drug_A", "drug_B", "drug_C"], n),
        "cell_line_id": np.random.choice([f"cell_{i}" for i in range(50)], n),
        "tissue": np.random.choice(["lung", "breast", "colon"], n),
        "AUC": np.random.rand(n)
    })
    
    evaluator = OODEvaluator(drug_response)
    
    train, test = evaluator.cold_drug_split()
    print(f"Train: {len(train)}, Test: {len(test)}")
    print(f"Test drugs: {test['drug_id'].unique()}")

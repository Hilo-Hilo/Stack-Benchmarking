"""
Baseline predictors for drug response prediction.
"""
from typing import Optional
import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score


class BaselinePredictor:
    """Base class for drug response predictors."""
    
    def __init__(self, model_type: str = "elastic_net", **kwargs):
        self.model_type = model_type
        self.kwargs = kwargs
        self.scaler = StandardScaler()
        self.model = None
        
    def _create_model(self):
        if self.model_type == "elastic_net":
            return ElasticNet(**self.kwargs)
        elif self.model_type == "random_forest":
            return RandomForestRegressor(**self.kwargs)
        elif self.model_type == "mlp":
            from sklearn.neural_network import MLPRegressor
            return MLPRegressor(**self.kwargs)
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def fit(self, X: np.ndarray, y: np.ndarray):
        """Fit the model."""
        X_scaled = self.scaler.fit_transform(X)
        self.model = self._create_model()
        self.model.fit(X_scaled, y)
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict drug response."""
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def cross_validate(
        self, 
        X: np.ndarray, 
        y: np.ndarray, 
        cv: int = 5,
        scoring: str = "r2"
    ) -> np.ndarray:
        """Cross-validate the model."""
        X_scaled = self.scaler.fit_transform(X)
        model = self._create_model()
        scores = cross_val_score(model, X_scaled, y, cv=cv, scoring=scoring)
        return scores


class DrugResponsePredictor:
    """Multi-drug response predictor using Stack embeddings."""
    
    def __init__(self, model_type: str = "elastic_net", **kwargs):
        self.predictors = {}
        self.model_type = model_type
        self.kwargs = kwargs
        
    def fit(
        self, 
        embeddings: np.ndarray, 
        drug_response: pd.DataFrame,
        drug_col: str = "drug_id",
        response_col: str = "AUC"
    ):
        """Fit predictors for each drug."""
        drugs = drug_response[drug_col].unique()
        
        for drug in drugs:
            mask = drug_response[drug_col] == drug
            X = embeddings[mask]
            y = drug_response.loc[mask, response_col].values
            
            if len(X) < 10:  # Skip drugs with too few samples
                continue
                
            predictor = BaselinePredictor(self.model_type, **self.kwargs)
            predictor.fit(X, y)
            self.predictors[drug] = predictor
            
        return self
    
    def predict(
        self, 
        embeddings: np.ndarray, 
        drug: str
    ) -> Optional[np.ndarray]:
        """Predict response for a specific drug."""
        if drug not in self.predictors:
            return None
        return self.predictors[drug].predict(embeddings)
    
    def evaluate(
        self,
        embeddings: np.ndarray,
        drug_response: pd.DataFrame,
        drug_col: str = "drug_id",
        response_col: str = "AUC",
        cv: int = 5
    ) -> dict:
        """Evaluate all drug predictors."""
        results = {}
        
        for drug in drug_response[drug_col].unique():
            mask = drug_response[drug_col] == drug
            X = embeddings[mask]
            y = drug_response.loc[mask, response_col].values
            
            if len(X) < cv + 1:
                continue
                
            predictor = BaselinePredictor(self.model_type, **self.kwargs)
            scores = predictor.cross_validate(X, y, cv=cv, scoring="r2")
            results[drug] = {
                "mean_r2": scores.mean(),
                "std_r2": scores.std(),
                "n_samples": len(X)
            }
            
        return results


def compute_baseline_predictions(
    drug_response: pd.DataFrame,
    embeddings: np.ndarray,
    method: str = "mean_drug"
) -> np.ndarray:
    """Compute simple baseline predictions."""
    
    if method == "mean_drug":
        # Mean response per drug
        baselines = drug_response.groupby("drug_id")["AUC"].mean().to_dict()
        predictions = np.array([baselines.get(d, np.mean(list(baselines.values()))) 
                                for d in drug_response["drug_id"]])
    elif method == "mean_cell":
        # Mean response per cell line
        baselines = drug_response.groupby("cell_line_id")["AUC"].mean().to_dict()
        predictions = np.array([baselines.get(c, np.mean(list(baselines.values()))) 
                                for c in drug_response["cell_line_id"]])
    elif method == "mean_drug_cell":
        # Mean drug + mean cell
        mean_drug = drug_response.groupby("drug_id")["AUC"].mean()
        mean_cell = drug_response.groupby("cell_line_id")["AUC"].mean()
        global_mean = drug_response["AUC"].mean()
        
        predictions = []
        for _, row in drug_response.iterrows():
            d_mean = mean_drug.get(row["drug_id"], global_mean)
            c_mean = mean_cell.get(row["cell_line_id"], global_mean)
            predictions.append((d_mean + c_mean) / 2)
        predictions = np.array(predictions)
    else:
        raise ValueError(f"Unknown baseline method: {method}")
    
    return predictions


if __name__ == "__main__":
    # Quick test
    # Generate dummy data
    n_samples = 1000
    n_features = 768  # Stack embedding dimension
    
    X = np.random.randn(n_samples, n_features)
    y = np.random.randn(n_samples)
    
    predictor = BaselinePredictor("elastic_net", alpha=0.1)
    scores = predictor.cross_validate(X, y, cv=5)
    print(f"CV R2 scores: {scores}")
    print(f"Mean R2: {scores.mean():.3f} +/- {scores.std():.3f}")

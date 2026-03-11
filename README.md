# Stack-Benchmarking

**Stack-first benchmarking for out-of-distribution cancer drug response prediction, with staged Evo 2 genotype augmentation**

Team: **Hanson Wen** (Molecular Bio + CS), **Nathan Gu** (EE + CS), **Foster Angus** (Applied Math)

---

## Overview

This project evaluates a simple question with strict benchmarking discipline:

> **Do Stack prompt-conditioned representations provide a real out-of-distribution (OOD) lift for perturbation + drug-response prediction, beyond strong baselines and non-ICL single-cell foundation models?**

Recent evidence suggests many complex drug-response models underperform or match simpler methods when evaluation is leakage-safe and truly OOD. We are testing whether Stack changes that outcome.

## Quick Start

### 1. Install Dependencies

```bash
# Clone repo
git clone https://github.com/Hilo-Hilo/Stack-Benchmarking.git
cd Stack-Benchmarking

# Set up Python environment (Python 3.9+)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install requirements
pip install -r requirements.txt

# Install Stack
git clone https://github.com/ArcInstitute/stack.git
cd stack
pip install -e .
cd ..
```

### 2. Download Model Checkpoints

See `checkpoints/README.md` for download instructions. You'll need:
- `bc_large.ckpt` - Stack-Large model (~2.5 GB)
- `basecount_1000per_15000max.pkl` - Gene list (~900 KB)

### 3. Prepare Data

Place your data in `data/raw/`:
- Single-cell expression: `*.h5ad` (AnnData format, HGNC gene symbols)
- Drug response: `*response*.csv`

### 4. Run Benchmark

```bash
python -m src.main --config configs/default.yaml
```

## Project Structure

```
Stack-Benchmarking/
├── checkpoints/       # Model weights (download from HuggingFace)
├── configs/           # Experiment configurations
├── data/
│   ├── raw/          # Original datasets
│   └── processed/    # Processed features/embeddings
├── src/
│   ├── data/         # Data loading & preprocessing
│   ├── models/       # Baseline predictors & Stack wrapper
│   └── eval/         # OOD evaluation & metrics
├── notebooks/        # Analysis notebooks
├── papers/           # Reference papers
└── PROPOSAL.md       # Original project proposal
```

## Method (3 Phases)

### Phase 1 — Perturbation-conditioned representation learning
- Inputs: pre-treatment query cells + prompt cells (drug, dose, time, tissue)
- Output: predicted post-treatment expression + perturbation-conditioned embeddings

### Phase 2 — Biological validity checks
- Score predicted expression with pathway collections (GSVA/ssGSEA)

### Phase 3 — Drug efficacy prediction
- Predict AUC/AAC using lightweight models (ElasticNet, XGBoost, MLP)

## Evaluation Policy (Leakage-Safe)

- Random + **cold-drug** + **cold-cell-line** splits
- Tissue/lineage-aware splits where possible
- Fixed-drug and fixed-cell aggregation reporting
- All preprocessing fit inside training folds only

## Baselines

- Raw or pseudo-bulk expression
- Standard drug descriptors (Morgan fingerprints)
- Marginal-effect baselines (mean-drug, mean-cell, mean(drug)+mean(cell))

## Requirements

- Python 3.9+
- PyTorch 2.0+
- Scanpy, anndata, scvi-tools
- Stack (`arc-stack`)

See `requirements.txt` for full list.

## License

Stack model weights: [Arc Research Institute Non-Commercial License](checkpoints/LICENSE)

## Contact

For questions, open an issue or contact the team.
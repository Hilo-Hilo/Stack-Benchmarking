# Stack-Benchmarking

**Stack-first benchmarking for out-of-distribution cancer drug response prediction, with staged Evo 2 genotype augmentation**

Team: **Hanson Wen** (Molecular Bio + CS), **Nathan Gu** (EE + CS), **Foster Angus** (Applied Math)

---

## Overview

This project evaluates a simple question with strict benchmarking discipline:

> **Do Stack prompt-conditioned representations provide a real out-of-distribution (OOD) lift for perturbation + drug-response prediction, beyond strong baselines and non-ICL single-cell foundation models?**

Recent evidence suggests many complex drug-response models underperform or match simpler methods when evaluation is leakage-safe and truly OOD. We are testing whether Stack changes that outcome.

---

## Project Aims

1. **OOD perturbation prediction**  
   Predict post-treatment expression from baseline query cells + perturbation prompts, then evaluate cold-drug / cold-cell generalization.

2. **Directional biology checks**  
   Verify predicted post-treatment transcriptomes move in biologically expected pathway / TF directions before training efficacy heads.

3. **Conditional efficacy prediction**  
   Test whether Stack-derived perturbation-conditioned features improve AUC/AAC drug efficacy prediction under leakage-safe OOD evaluation.

4. **Stretch goal**  
   Late-fuse **Evo 2 genotype embeddings** with Stack features if Phases 1-3 show reproducible OOD lift.

---

## Method (3 Phases)

### Phase 1 — Perturbation-conditioned representation learning
- Inputs:
  - pre-treatment "query" cells
  - prompt cells encoding **drug, dose, time, tissue context**
- Model output:
  - predicted post-treatment expression profiles
  - perturbation-conditioned embeddings
- Metrics:
  - Pearson / R²
  - compound-level aggregation metrics
- Splits:
  - held-out, cold-drug, cold-cell where feasible

### Phase 2 — Biological validity checks
- Score predicted expression with pathway/signature collections
- Methods:
  - GSVA / ssGSEA
  - single-cell-appropriate signature scoring
  - pathway / TF activity inference
- Goal:
  - ensure representations are biologically meaningful before efficacy modeling

### Phase 3 — Drug efficacy prediction
- Predict endpoints per (cell line, drug):
  - primary: **AUC / AAC**
  - secondary (when suitable): IC50 and/or binarized sensitivity
- Lightweight predictors:
  - Elastic Net
  - XGBoost / LightGBM
  - shallow MLP
- Controlled ablations:
  - add Stack-conditioned features on top of strong baselines

---

## Evaluation Policy (Leakage-Safe by Design)

We prioritize robustness and anti-leakage protocol:

- random + **cold-drug** + **cold-cell-line** splits
- tissue / lineage-aware splits where possible
- fixed-drug and fixed-cell aggregation reporting
- all preprocessing fit **inside training folds only**
- optional cross-dataset transfer checks for distribution shift stress testing

Baselines include:
- raw or pseudo-bulk expression
- standard drug descriptors (e.g., Morgan fingerprints)
- marginal-effect baselines (mean-drug, mean-cell, mean(drug)+mean(cell))

---

## Datasets (Planned)

- Single-cell perturbation datasets suitable for Stack-style conditioning (including Tahoe-100M style resources)
- Cancer drug response resources for efficacy endpoints (e.g., CCLE/GDSC-compatible settings)
- Optional paired cohort for stretch phase (e.g., BeatAML2) for genotype fusion

---

## Repo Status

This repository currently tracks the proposal-driven project setup and will be expanded with:

- `data/` ingestion + preprocessing pipelines
- `src/` modeling and evaluation code
- `configs/` split definitions and experiment configs
- `notebooks/` exploratory and analysis notebooks
- reproducible experiment logs + benchmark tables

---

## References

Key references from proposal (abbrev.):

1. scDrugMap (2025)  
2. Tahoe-100M perturbation atlas (2025)  
3. Wang et al., Nat Comput Sci (2026)  
4. Wei et al., Nat Methods (2026)  
5. Chawla et al., Nat Commun (2022)  
6. Schubert et al., Nat Commun (2018)  
7. Codicè et al., J Cheminformatics (2025)  
8. Branson et al., Bioinformatics (2025)  
9. Partin et al., Brief Bioinform (2026)  
10. Asiaee et al., leakage preprint (2026)  
11. Bottomly et al., Cancer Cell (2022)  
12. Sharifi-Noghabi et al., MOLI (2019)

---

## Contact

For collaboration or review discussions, open an issue in this repo or contact the team directly.

# Stack-first benchmarking for out-of-distribution cancer drug response prediction, with staged Evo 2 genotype augmentation

Team (Benign Bears): Hanson Wen, Nathan Gu, Foster Angus

### Motivation and Problem

Recent evaluations of complex deep models for drug-response predictions demonstrate little improvement compared to simple baselines with proper evaluation. Foundation models for single‑cell and bulk expression similarly fail to consistently beat raw expression under distribution shift. We ask the question: **Do Stack's prompt-conditioned representations provide a real out-of-distribution (OOD) lift for drug perturbation + drug-response prediction, beyond strong baselines and non-ICL single-cell foundation models?** We have started working on the following: [*https://github.com/Hilo-Hilo/Stack-Benchmarking*](https://github.com/Hilo-Hilo/Stack-Benchmarking)

### Project Aims

**OOD perturbation prediction**: predict post-treatment expression from baseline query cells + perturbation prompts and quantify cold-drug / cold-cell generalization. 

**Directional biology checks**: verify predicted responses shift the right pathways/TF programs before training efficacy heads.

**Efficacy prediction (conditional)**: test whether Stack-derived perturbation-conditioned features improve AUC/AAC prediction under leakage-safe OOD evaluation.

**Stretch**: late-fuse Evo 2 genotype embeddings with Stack features if Phases 1–3 show a reproducible lift.

### Methology

We attempt the answer the research question via a 3 phase plan: 

**Phase 1** aims to establish a method to obtain a drug-conditioned representation of a cell line's transcriptomic state. The inputs are (a) pre‑treatment "query" cells from a given cell line and (b) a "prompt" cell encoding drug, dose, time, and tissue context). Stack outputs drug-conditioned gene expression profiles and embeddings. Instead of fine-tuning model weights, we condition on a prompt cell that encodes the perturbation context (drug, dose, time, tissue) and examine whether this conditioning meaningfully shifts the predicted transcriptome.

Although most labeled cancer drug-response datasets (GDSC/CCLE) are largely bulk seq in contrast to Stack's single-cell resolution input, there exist datasets curated for single cell foundational model benchmarking, including pre/post drug perturbation scRNA-Seq data. We will benchmark predicted gene expressions using Held-out splits, Pearson / R² correlation, and Compound-level aggregation, against models outlined in the research question above. 

For **Phase 2**, before training any efficacy predictor, we will test whether the predicted post-treatment transcriptomes move in the biologically expected direction. We will score them against curated pathway and signature collections using GSVA/ssGSEA and single‑cell‑appropriate signature methods, and we will infer pathway and transcription factor activity. These approaches are widely used for interpreting transcriptomic perturbations and have direct precedent for linking perturbation signatures to viability and drug sensitivity. We will apply these existing methods to Stack produced results. 

In **Phase 3**, we will train lightweight predictors (Elastic Net; XGBoost/LightGBM; shallow MLP) to predict drug efficacy for each (cell line, drug) pair, using AUC/AAC as primary endpoints (IC50 and/or binarized sensitivity as secondary when appropriate). To ensure gains reflect real generalization rather than shortcut learning, we will benchmark against strong baselines: raw or pseudo-bulk expression, standard drug descriptors (e.g., Morgan fingerprints), and marginal-effect models (mean-drug, mean-cell, mean(drug)+mean(cell)). We then add Stack-derived perturbation‑conditioned embeddings from Phase 1 and quantify their incremental value via controlled ablations.

Evaluation will prioritize robustness: random, cold-drug, cold-cell-line, and tissue/lineage-aware splits (when feasible), and we will include fixed‑drug and fixed‑cell aggregation. All preprocessing (scaling, gene filtering, dimensionality reduction, feature selection) will be fit strictly within training folds using end-to-end pipelines to prevent leakage. Where feasible, we will add a cross‑dataset transfer check (train on one screen, test on another) to stress-test robustness under distribution shift.

**Stretch**: If Stack features demonstrate a reproducible OOD lift, we will test whether late‑fused Evo 2 genotype embeddings improve performance on a paired patient cohort (e.g., BeatAML2) using the same lightweight predictors with strong regularization. 

### Fellowship Goals and Team Fit

We have been following published works from Arc for a long time. This would be an incredible opportunity to work on something this team **truly cares about**. Everyone in this team desires to work on AIxBio topics in the future, with foundation models being a strong topic of interest. We want to understand when foundation models actually help in biological prediction and when simpler methods are enough. A stretch goal would be to understand the trade-off between fully self supervised learning and biologically informed biological models. Our team of 3 had a great time teaming previously on various projects, from iGEM to hackathons. The brainstorming of this project refined our collaboration further. We love working and each other and we are **fully dedicated** to bringing this project to life whilst working with Arc. 

### References

1. scDrugMap: Single-cell drug response prediction using attention-based neural networks. (2025).
2. Tahoe (Vevo Therapeutics). Tahoe-100M: A Giga-Scale Single-Cell Perturbation Atlas for Context-Dependent Gene Function and Cellular Modeling. bioRxiv (2025).
3. Wang, Y. et al. Predicting drug responses of unseen cell types through transfer learning with foundation models. Nat. Comput. Sci. 6, 39–52 (2026).
4. Wei, Z. et al. Benchmarking algorithms for generalizable single-cell perturbation response prediction. Nat. Methods 23, 451–464 (2026).
5. Chawla, S. et al. Gene expression based inference of cancer drug sensitivity. Nat. Commun. 13, 5680 (2022).
6. Schubert, M. et al. Perturbation-response genes reveal signaling footprints in cancer gene expression. Nat. Commun. 9, 20 (2018).
7. Codicè, F. et al. The specification game: rethinking the evaluation of drug response prediction for precision oncology. J. Cheminformatics 17, 33 (2025).
8. Branson, N., Cutillas, P. R. & Bessant, C. Understanding the sources of performance in deep drug response models reveals insights and improvements. Bioinformatics 41, i142–i149 (2025).
9. Partin, A. et al. Benchmarking community drug response prediction models: datasets, models, tools, and metrics for cross-dataset generalization analysis. Brief. Bioinform. 27, bbaf667 (2026).
10. Asiaee, A. et al. Widespread data leakage inflates performance estimates in cancer drug response prediction. Preprint at https://doi.org/10.64898/2026.02.05.704016 (2026).
11. Bottomly, D. et al. Integrative analysis of drug response and clinical outcome in acute myeloid leukemia. Cancer Cell 40, 850-864.e9 (2022).
12. Sharifi-Noghabi, H., Zolotareva, O., Collins, C. C. & Ester, M. MOLI: multi-omics late integration with deep neural networks for drug response prediction. Bioinformatics 35, i501–i509 (2019).
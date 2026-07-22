# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Research code for *"Spectral Clustering Identifies Three Clinical HFpEF Phenotypes in Thai Patients"*. The pipeline clusters HFpEF (Heart Failure with preserved Ejection Fraction) patients using Spectral Clustering, KMeans, and Gaussian Mixture Models, then statistically characterizes the resulting phenotypes.

## Running Notebooks

All notebooks are run interactively in Jupyter. Launch with:

```
jupyter notebook
```

Notebooks depend on Excel data files (`HFpEF-research_100.xlsx`, `HFpEF-research_200.xlsx`, `HFpEF-research-4.4.xlsx` for the 405-patient cohort) that are **not committed to the repo** — they must be present in the working directory at runtime.

## Architecture

### Python Modules

- **`preproc.py`** — Data loaders. Key functions:
  - `get_hfpef_100()` / `get_hfpef_100_nomiss_selected_feats()` — load and clean the 100-patient dataset
  - `get_hfpef_200(nomiss=False)` — load and clean the 200-patient dataset; handles NTProBNP string values (`>35,000` → 35001), LV mass index typo (`183,7` → 183.7), imputes LA diameter / LAVI using the formula from [doi:10.1111/echo.14943](https://onlinelibrary.wiley.com/doi/full/10.1111/echo.14943)
  - `get_hfpef_405(nomiss=False, get_mortal_hospitalize=False, get_patient_no=False)` — load and clean the 405-patient dataset (`HFpEF-research-4.4.xlsx`); shares the 200-patient cleaning/imputation logic and adds an `HT` (hypertension) feature. `get_mortal_hospitalize=True` retains time-to-event/censor columns (death, HF re-hospitalization, MACE) instead of dropping them, for survival analysis; `get_patient_no=True` returns participant IDs as a separate `df_pnum`
  - `convert2np(df, lbl_colname, selected_feat=0)` — splits a DataFrame into `(X, y, feature_list)` numpy arrays; `selected_feat` is an int: `0`=all features, `1`=the 13 expert-selected features, `2`=`['NTProBNP']` only

- **`methods.py`** — Clustering wrappers and statistical characterization:
  - `get_km_pred`, `get_sc_pred`, `get_gm_pred` — uniform `(k, X) → labels` interface for KMeans, SpectralClustering (`arpack` solver, `nearest_neighbors` affinity), and GaussianMixture
  - `get_p_ci(data_df, y_pred)` — returns `(feat_df, cluster_df)` with p-values (ANOVA for continuous, chi-square for categorical) and per-cluster means / 95% CIs

- **`utils.py`** — Evaluation metrics and plots:
  - `get_score(k, f, X, y_true)` — computes silhouette, Davies-Bouldin, Calinski-Harabasz, homogeneity/completeness/V-measure, rand/mutual info scores for a given clustering function `f`
  - `plot_clustering_score`, `plot_contingency_matrix`, `plot_bic_aic`, `plot_data` — visualization helpers used by notebooks

### Notebook Pipeline (200-patient, primary analysis)

1. **`preprocess_data.ipynb`** — Exploratory cleaning; outputs saved as PNG (tsne_200.png, pca_200.png, spectral_clustering_200.png)
2. **`cluster_hfpef-200.ipynb`** — Main clustering comparison: all features vs. selected features, across k=2–7, three methods. Exports results to `HFpEF_allfeat_spectral_3clus_200samples.xlsx` and `HFpEF_selfeat_spectral_2clus_200samples.xlsx`
3. **`cluster_hfpef_viz-200.ipynb`** — Visualizes final cluster assignments
4. **`classify_hfpef-200.ipynb`** — Trains classifiers to predict cluster membership
5. **`cluster_analysis.ipynb`** / **`test_cluster_analysis.ipynb`** — Statistical characterization of clusters using `get_p_ci`

The 100-patient notebooks (`cluster_hfpef.ipynb`, `cluster_hfpef_viz.ipynb`, `classify_hfpef.ipynb`) mirror the same pipeline on the earlier, smaller dataset. `cluster_hfpef_lca.ipynb` runs Latent Class Analysis as an alternative method.

### Notebook Pipeline (405-patient)

1. **`preprocess_data-405.ipynb`** — Exploratory cleaning; t-SNE/PCA/Isomap and SpectralClustering visualization
2. **`cluster_hfpef-405.ipynb`** — Clustering comparison: all features, selected features, PCA-selected features, and cleaned data, across k=2–7, three methods. Exports `HFpEF_allfeat_spectral_3clus_405samples.xlsx`, `HFpEF_selfeat_spectral_3clus_405samples.xlsx`
3. **`cluster_hfpef_viz-405.ipynb`** — Visualizes final cluster assignments
4. **`classify_hfpef-405.ipynb`** — Trains classifiers (RandomForest, MLP) to predict cluster membership
5. **`cluster_analysis-405.ipynb`** — Statistical characterization of clusters using `get_p_ci`; exports `HFpEF_onefeat_spectral_3clus_405samples.xlsx` alongside the files from step 2
6. **`kaplan_meier_curve-405.ipynb`** — Kaplan-Meier survival analysis (`lifelines`) per cluster, reading cluster assignments back from the step 5 output files. Covers three outcomes: all-cause death, HF re-hospitalization, and MACE, each as a time-to-event/censor pair

### Key Constants

- **Selected features** (defined in `preproc.py:selected_feats`): Age, Sex, Cr, GFR, CKD stage, AF, MAP, PP, NTProBNP, medial a′, medial E′, LAVI, LA diameter
- **Outcome labels**: Death, CV death, Major cardiac events
- SpectralClustering always uses `eigen_solver='arpack'`, `affinity='nearest_neighbors'`, `random_state=0`
- Feature type threshold in `get_p_ci`: ≤8 unique values → treated as categorical (chi-square), otherwise continuous (one-way ANOVA)

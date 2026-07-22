# HFpEF-clustering

Source code for *Spectral Clustering Identifies Three Clinical HFpEF Phenotypes in Thai Patients*

## Getting Started

The main analysis notebook is **`cluster_hfpef-200.ipynb`** and **`cluster_hfpef-405.ipynb`**, which runs Spectral Clustering, KMeans, and Gaussian Mixture Models across a range of k values on the 200-patient and 405-patient datasets respectively and exports the results.

To reproduce the final cluster assignments and analyses used in the manuscript, run the following notebooks in order:

1. Run **`cluster_analysis-405.ipynb`** end to end. It loads the 405-patient cohort via `get_hfpef_405` function, runs Spectral Clustering (k=3) for three feature sets (all features, 13 expert-selected features, NTProBNP only).
2. Run **`cluster_hfpef_viz-405.ipynb`** to visualize the final cluster assignments for each of the three feature sets.
3. Run **`kaplan_meier_curve-405.ipynb`**. It reloads the same cohort via `get_hfpef_405` function, re-runs the same three clusterings, and asserts each one exactly reproduces the cluster assignments written in step 1 before plotting Kaplan-Meier survival curves per cluster.
4. Run **`cluster_analysis-405.ipynb`** to calculate the significance of differences between clusters and export the final cluster statistics to `.xlsx` for manuscript tables.


## Repository Organization

### Notebooks (200-patient cohort)

| Notebook | Description |
|---|---|
| `preprocess_data.ipynb` | Data cleaning and dimensionality reduction exploration (t-SNE, PCA) |
| `cluster_hfpef-200.ipynb` | **Main analysis** — clustering comparison on patient dataset, exports results to `.xlsx` |
| `cluster_hfpef_viz-200.ipynb` | Visualization of final cluster assignments |
| `classify_hfpef-200.ipynb` | Classification models to predict cluster membership |
| `cluster_analysis.ipynb` | Statistical characterization of clusters (p-values, means, 95% CIs) |
| `test_cluster_analysis.ipynb` | Validation of cluster analysis |
| `cluster_hfpef_lca.ipynb` | Alternative approach using Latent Class Analysis |

### Notebooks (405-patient cohort)

| Notebook | Description |
|---|---|
| `preprocess_data-405.ipynb` | Exploratory cleaning; t-SNE/PCA/Isomap and SpectralClustering visualization |
| `cluster_hfpef-405.ipynb` | Clustering comparison (all/selected/PCA-selected features, k=2–7, three methods) |
| `cluster_hfpef_viz-405.ipynb` | Visualization of final cluster assignments |
| `classify_hfpef-405.ipynb` | Classification models (RandomForest, MLP) to predict cluster membership |
| `cluster_analysis-405.ipynb` | **Main analysis** — statistical characterization of clusters, exports results to `.xlsx` |
| `kaplan_meier_curve-405.ipynb` | Kaplan-Meier survival analysis per cluster (death, HF re-hospitalization, MACE) |


### Scripts

| File | Description |
|---|---|
| `preproc.py` | Data loaders and preprocessing for patient datasets |
| `methods.py` | Clustering method wrappers and statistical analysis (`get_p_ci`) |
| `utils.py` | Evaluation metrics and plotting helpers |

### Outputs

| File | Description |
|---|---|
| `HFpEF_allfeat_spectral_3clus_200samples.xlsx` | 200-patient cohort: cluster assignments using all features (3 clusters) |
| `HFpEF_selfeat_spectral_2clus_200samples.xlsx` | 200-patient cohort: cluster assignments using selected features (2 clusters) |
| `HFpEF_allfeat_spectral_3clus_405samples_wKM.xlsx` | 405-patient cohort: cluster assignments using all features (3 clusters), cross-validated against `kaplan_meier_curve-405.ipynb` |
| `HFpEF_selfeat_spectral_3clus_405samples_wKM.xlsx` | 405-patient cohort: cluster assignments using the 13 expert-selected features (3 clusters), cross-validated against `kaplan_meier_curve-405.ipynb` |
| `HFpEF_onefeat_spectral_3clus_405samples_wKM.xlsx` | 405-patient cohort: cluster assignments using NTProBNP only (3 clusters), cross-validated against `kaplan_meier_curve-405.ipynb` |

## Requirements

```
pip install -r requirements.txt
```

Key libraries:
- **scikit-learn** — clustering algorithms (Spectral Clustering, KMeans, GMM) and evaluation metrics
- **openpyxl** — required by pandas to read/write `.xlsx` data files
- **rpy2** — Python-R bridge, used only in `cluster_hfpef_lca.ipynb` to run R-based Latent Class Analysis

## Citation

T. Amphanet*; A. Buakhamsri; S. Gulyanon. **Spectral Clustering Identifies Three Clinical HFpEF Phenotypes in Thai Patients**. 2026.
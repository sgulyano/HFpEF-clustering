# HFpEF-clustering

Source code for *Spectral Clustering Identifies Three Clinical HFpEF Phenotypes in Thai Patients*

## Getting Started

The main analysis notebook is **`cluster_hfpef-200.ipynb`**, which runs Spectral Clustering, KMeans, and Gaussian Mixture Models across a range of k values on the 200-patient dataset and exports the results.

## Repository Organization

### Notebooks

| Notebook | Description |
|---|---|
| `preprocess_data.ipynb` | Data cleaning and dimensionality reduction exploration (t-SNE, PCA) |
| `cluster_hfpef-200.ipynb` | **Main analysis** — clustering comparison on patient dataset, exports results to `.xlsx` |
| `cluster_hfpef_viz-200.ipynb` | Visualization of final cluster assignments |
| `classify_hfpef-200.ipynb` | Classification models to predict cluster membership |
| `cluster_analysis.ipynb` | Statistical characterization of clusters (p-values, means, 95% CIs) |
| `test_cluster_analysis.ipynb` | Validation of cluster analysis |
| `cluster_hfpef_lca.ipynb` | Alternative approach using Latent Class Analysis |

### Scripts

| File | Description |
|---|---|
| `preproc.py` | Data loaders and preprocessing for patient datasets |
| `methods.py` | Clustering method wrappers and statistical analysis (`get_p_ci`) |
| `utils.py` | Evaluation metrics and plotting helpers |

### Outputs

| File | Description |
|---|---|
| `HFpEF_allfeat_spectral_3clus_200samples.xlsx` | Cluster assignments using all features (3 clusters) |
| `HFpEF_selfeat_spectral_2clus_200samples.xlsx` | Cluster assignments using selected features (2 clusters) |

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
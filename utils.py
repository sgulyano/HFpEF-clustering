import numpy as np
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt

from sklearn.mixture import GaussianMixture
from sklearn.manifold import TSNE
from sklearn.metrics.cluster import silhouette_score, davies_bouldin_score
from sklearn.metrics.cluster import homogeneity_score, completeness_score, v_measure_score
from sklearn.metrics.cluster import calinski_harabasz_score, homogeneity_completeness_v_measure
from sklearn.metrics.cluster import contingency_matrix, rand_score, mutual_info_score
from sklearn.metrics.cluster import adjusted_mutual_info_score, adjusted_rand_score

score_columns = ['k', 'silhouette', 'davies', 'homogeneity',
                 'completeness', 'vmeasure', 'calinski', 
                 'rand index', 'mutual info', 'ami', 
                 'adjusted rand', 'contingency matrix', 'counts']

def get_score(k, f, X, y_true):
    y_pred = f(k, X)
    _, counts = np.unique(y_pred, return_counts=True)
    
    sil = silhouette_score(X, y_pred)
    db = davies_bouldin_score(X, y_pred)
    hom = homogeneity_score(y_true, y_pred)
    com = completeness_score(y_true, y_pred)
    vms = v_measure_score(y_true, y_pred)
    cal = calinski_harabasz_score(X, y_pred)
    rand = rand_score(y_true, y_pred)
    mi = mutual_info_score(y_true, y_pred)
    ami = adjusted_mutual_info_score(y_true, y_pred)
    ar = adjusted_rand_score(y_true, y_pred)
    cmat = contingency_matrix(y_true, y_pred)
    return k, sil, db, hom, com, vms, cal, rand, mi, ami, ar, cmat, counts




def plot_clustering_score(all_dfs, methods, lbl_colname):
    x = 'k'
    feats = ['silhouette', 'davies', 'homogeneity', 'completeness', 'vmeasure', 'calinski', 'rand index', 'mutual info', 'ami', 'adjusted rand']
    fig, axes = plt.subplots(len(feats), 3, figsize=(14, 30))
    for l, y1 in enumerate(feats):
        for i, lbl in enumerate(lbl_colname):
            for j, met in enumerate(methods):
                axes[l,i].plot(all_dfs[j][i][x], all_dfs[j][i][y1], label=met)
            axes[l,i].set_title(f'{lbl}')
            axes[l,i].set_xlabel(x)
            axes[l,i].tick_params(axis='y')
        axes[l,0].legend()
        axes[l,0].set_ylabel(y1)
        plt.tight_layout()

def plot_contingency_matrix(all_dfs, methods, lbl_colname):
    for j, met in enumerate(methods):
        n = len(all_dfs[j][0]['contingency matrix'])
        for l in range(n):
            fig, axes = plt.subplots(1, 3, figsize=(14, 3))
            fig.suptitle(f"{met}, k={all_dfs[j][0]['k'][l]}")
            for i, lbl in enumerate(lbl_colname):
                t = all_dfs[j][i]['contingency matrix'][l]
                df_cm = pd.DataFrame(t, 
                          index = np.arange(t.shape[0]),
                          columns = np.arange(t.shape[1]))
                res = sn.heatmap(df_cm, annot=True, vmin=0.0, cmap="Blues", ax=axes[i])
                res.set_ylabel(lbl)
                res.set_xlabel('cluster')
            plt.tight_layout()


def plot_bic_aic(X, no_clusters=12):
    bics = []
    aics = []
    for nc in range(2,no_clusters):
        gm = GaussianMixture(n_components=nc, random_state=0, init_params='kmeans').fit(X)
        y_pred = gm.predict(X)
        bics.append(gm.bic(X))
        aics.append(gm.aic(X))
    
    plt.plot(range(2,12), bics)
    plt.plot(range(2,12), aics)
    plt.xlabel('# clusters')
    plt.legend(['bic','aic'])
    plt.title(f'GMM BIC and AIC\nBIC={min(bics):.3f},\nAIC={min(aics):.3f}')
    plt.show()
    return bics, aics


def plot_data(X, y, no_clusters, fs, lbl_colname):
    X_embedded = TSNE(n_components=2, init='random').fit_transform(X)
    fig, axes = plt.subplots(1, len(y[0]), figsize=(15, 4))
    for i in range(len(y[0])):
        scatter = axes[i].scatter(X_embedded[:, 0], X_embedded[:, 1], c=y[:,i], 
                                  cmap=plt.cm.coolwarm, alpha=0.5)
#         axes[i].set_xticks([])
#         axes[i].set_yticks([])
#         axes[i].set_aspect('equal')
        axes[i].legend(scatter.legend_elements()[0], ['No','Yes'], title="Classes")
        axes[i].set_title(f'{lbl_colname[i]}')
    
    fig, axes = plt.subplots(no_clusters-2, len(fs), figsize=(15, 4*(no_clusters-2)))
    for k in range(2, no_clusters):
        for i, (name, f) in enumerate(fs.items()):
            y_pred = f(k, X)
            scatter = axes[k-2,i].scatter(X_embedded[:, 0], X_embedded[:, 1], c=y_pred, 
                                          cmap=plt.cm.Set2, alpha=0.5,
                                          vmin=0, vmax=no_clusters-1)
            axes[k-2,i].legend(*scatter.legend_elements())
            axes[k-2,i].set_title(f'{name}, k={k}')
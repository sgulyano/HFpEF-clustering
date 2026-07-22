import numpy as np
import pandas as pd

from scipy.stats import f_oneway, chi2_contingency
import scipy.stats as st

from sklearn.metrics.cluster import contingency_matrix
from sklearn.cluster import SpectralClustering, KMeans
from sklearn.mixture import GaussianMixture

def get_km_pred(k, X):
    km = KMeans(n_clusters=k, random_state=0)
    return km.fit_predict(X)

def get_sc_pred(k, X):
    sc = SpectralClustering(n_clusters=k, eigen_solver='arpack', affinity="nearest_neighbors", random_state=0)
    return sc.fit_predict(X)

def get_gm_pred(k, X):
    gm = GaussianMixture(n_components=k, random_state=0, init_params='kmeans').fit(X)
    return gm.predict(X)


def get_p_ci(data_df, y_pred):
    # Initialize feature DataFrame
    feat_df = pd.DataFrame({'p-value':0.0, 'is_category':False}, index=data_df.columns)
    
    # Determine whether the feature is continuous or discrete
    for col in data_df:
        if data_df[col].unique().shape[0] <= 8:
            data_df[col] = data_df[col].astype('int')
            feat_df.loc[col,'is_category'] = True
    
    # Compute p-value for continuous features
    cont_cols = feat_df[~feat_df['is_category']].index
    clusters = []
    for yi in np.unique(y_pred):
        idx = y_pred == yi
        clusters.append(data_df.loc[idx, cont_cols])
    F, p = f_oneway(*clusters)
    feat_df.loc[cont_cols, 'p-value'] = p
    
    # Compute p-value for category features
    cat_cols = feat_df[feat_df['is_category']].index
    for cat_col in cat_cols:
        obs = contingency_matrix(y_pred, data_df[cat_col])
        chi2, p, dof, ex = chi2_contingency(obs.T, correction=False)
        feat_df.loc[cat_col,'p-value'] = p
    
    # Initialize cluster DataFrame
    ind = ['n'] + [f'{c}_{v}' for c in cat_cols for v in np.unique(data_df[c])] + list(cont_cols)
    pat = {f'{yi}_{s}':0 for yi in np.unique(y_pred) for s in ['mu', 'ci_l', 'ci_h']}
    pat['p-value'] = 0.0

    cluster_df = pd.DataFrame(pat, index=ind)
    
    # Compute mean and CI for continuous features
    # https://www.statology.org/confidence-intervals-python/
    for yi in np.unique(y_pred):
        idx = y_pred == yi
        data_arr = data_df.loc[idx, cont_cols]
        ci = st.norm.interval(confidence=0.95, loc=np.mean(data_arr), scale=st.sem(data_arr))
        cluster_df.loc[cont_cols, f'{yi}_mu'] = np.mean(data_arr)
        cluster_df.loc[cont_cols, f'{yi}_ci_l'] = ci[0]
        cluster_df.loc[cont_cols, f'{yi}_ci_h'] = ci[1]
        cluster_df.loc[cont_cols, 'p-value'] = feat_df.loc[cont_cols, 'p-value']
    
    # Compute count and ratio for discrete features
    for yi in np.unique(y_pred):
        n = sum(y_pred == yi)
        cluster_df.loc['n', f'{yi}_mu'] = n
        idx = y_pred == yi
        for c in cat_cols:
            for v in np.unique(data_df[c]):
                mu = sum(data_df.loc[idx, c] == v)
                cluster_df.loc[f'{c}_{v}', f'{yi}_mu'] = mu
                cluster_df.loc[f'{c}_{v}', f'{yi}_ci_l'] = (mu / n) * 100
                cluster_df.loc[f'{c}_{v}', 'p-value'] = feat_df.loc[c, 'p-value']

    return feat_df, cluster_df

    
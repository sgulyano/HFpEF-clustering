import pandas as pd
import numpy as np
import warnings

selected_feats = ['Age', 'Sex', 'Cr', 'GFR', 'CKD stage', 'AF', 'MAP', 'PP', 'NTProBNP', "medial a'", "medial E'", 'LAVI', 'LA diameter']

def get_hfpef_100():
    """ HFpEF Dataset of 100 patients with all available features
    """ 
    df = pd.read_excel('HFpEF-research_100.xlsx', skiprows=[1,2,3,4,5,6])
    # drop unused features
    df = df.drop(columns=['Unnamed: 0', 'time to mortality after diagnosis', 'time to HF hospitalization after diagnosis'])
    df = df.copy()
    # drop 2 records that have many missing values
    df = df.dropna(subset=['SBP', 'DBP'])
    # fix NTProBNP when over 35,000 (machine limits)
    df.loc[df['NTProBNP']=='>35,000','NTProBNP'] = 35001
    df.loc[df['NTProBNP']=='> 35000','NTProBNP'] = 35001
    df['NTProBNP'] = df['NTProBNP'].astype('float')
    # fix missing data by filling with 0
    df = df.fillna(0)
    return df


def get_hfpef_100_nomiss_selected_feats():
    """ HFpEF Dataset of 100 patients and filter out records with missing values with only hand-picked features
    """ 
    df = pd.read_excel('HFpEF-research_100.xlsx', skiprows=[1,2,3,4,5,6])
    # keep only selected features, picked by experts
    df = df[['Age', 'Sex', 'Cr', 'GFR', 'CKD stage', 'AF', 'MAP', 'PP', 'NTProBNP', "medial a'", "medial E'", 'LAVI', 'LA diameter', 'Death', 'CV death', 'HF hospitalization']]
    # clean missing data by filling with 0 for LAVI and LA diameter
    df = df.copy()
    df['LAVI'] = df['LAVI'].fillna(0)
    df['LA diameter'] = df['LA diameter'].fillna(0)
    # fix NTProBNP when over 35,000 (machine limits)
    df.loc[df['NTProBNP']=='>35,000','NTProBNP'] = 35001
    df.loc[df['NTProBNP']=='> 35000','NTProBNP'] = 35001
    df['NTProBNP'] = df['NTProBNP'].astype('float')
    # drop missing records
    df.dropna(inplace=True)
    return df

def convert2np(df, lbl_colname, selected_feat=0):
    """ Convert the HPpEF DataFrame into NumPy array with 'lbl_colname' as label
    """
    y = np.array(df[lbl_colname])#.ravel()
    X = df.drop(lbl_colname, axis = 1)
    if type(selected_feat)==bool:
        raise Exception('selected_feat must an integer. It must be either 0, 1, or 2.')
    if selected_feat == 1:
        X = X[['Age', 'Sex', 'Cr', 'GFR', 'CKD stage', 'AF', 'MAP', 'PP', 'NTProBNP', "medial a'", "medial E'", 'LAVI', 'LA diameter']]
    elif selected_feat == 2:
        X = X[['NTProBNP']]
    elif selected_feat == 0:
        warnings.warn("Warning...........selected_feat is not given, set to 0 where all features are used.")
    else:
        raise Exception('Unknown selected_feat. It must be either 0, 1, or 2.')
    # Saving feature names for later use
    feature_list = list(X.columns)
    # # Convert to numpy array
    return np.array(X), y, feature_list


def get_hfpef_200(nomiss = False):
    """ HFpEF Dataset of 200 patients with all available features
    """ 
    df = pd.read_excel('HFpEF-research_200.xlsx', skiprows=[1,2,3,4,5,6,7,8,9])
    # drop unused features (use Major cardiac events instead of HF re-hospitalization)
    df = df.drop(columns=['Unnamed: 0', 'time to mortality after diagnosis', 'time to HF hospitalization after diagnosis', 'SSRI', 'HF re-hospitalization'])
    df = df.copy()
    # fix AF (typo 9 to 0)
    df.loc[df['AF']==9,'AF'] = 0
    # fix NTProBNP when over 35,000 (machine limits)
    df.loc[df['NTProBNP']=='>35,000','NTProBNP'] = 35001
    df.loc[df['NTProBNP']=='> 35000','NTProBNP'] = 35001
    df.loc[df['NTProBNP']=='>35000','NTProBNP'] = 35001
    df['NTProBNP'] = df['NTProBNP'].astype('float')
    # fix LV mass index typo (, to .)
    df.loc[df['LV mass index']=='183,7','LV mass index'] = 183.7
    df['LV mass index'] = df['LV mass index'].astype('float')
    # fix missing data of BMI, BSA, HR with mean values
    df['BMI'] = df['BMI'].fillna(df['BMI'].mean())
    df['BSA'] = df['BSA'].fillna(df['BSA'].mean())
    df['HR'] = df['HR'].fillna(df['HR'].mean().round())
    # Fix LA diameter using formula from https://onlinelibrary.wiley.com/doi/full/10.1111/echo.14943
    # LA diameter = 10.7 + 0.27 * LAVI + 10.6 * BSA
    idx = df['LA diameter'].isnull()
    df.loc[idx, 'LA diameter'] = (10.7 + (0.27 * df['LAVI'][idx]) + (10.6 * df['BSA'][idx])) / 10
    
    if nomiss:
        df['smoke'] = df['smoke'].fillna(0)
        df['stroke'] = df['stroke'].fillna(0)
        # drop missing records
        df.dropna(inplace=True)
    else:
        # fix missing data by filling with 0
        df = df.fillna(0)
    return df


def get_hfpef_405(nomiss = False, get_mortal_hospitalize = False, get_patient_no = False):
    """ HFpEF Dataset of 405 patients with all available features, which has an extra feature, HT
    """ 
    df = pd.read_excel('HFpEF-research-4.4.xlsx', skiprows=[1,2,3,4,5,6,7,8,9])
    # drop unused features (use Major cardiac events instead of HF re-hospitalization)
    if get_mortal_hospitalize:
        df = df.drop(columns=['SSRI'])
        df['time to mortality after diagnosis'] = df['time to mortality after diagnosis'].fillna(-1)
        df['time to HF hospitalization after diagnosis'] = df['time to HF hospitalization after diagnosis'].fillna(-1)
        df['time to MACE'] = df['time to MACE'].fillna(-1)
        df.loc[df['censor (HF)']==11, 'censor (HF)'] = 1
    else:
        df = df.drop(columns=['time to mortality after diagnosis', 
                              'time to HF hospitalization after diagnosis', 
                              'SSRI', 
                              'censor (death)', 
                              'censor (HF)', 
                              'censor (MACE)', 
                              'time to MACE'])
        
    df = df.copy()
    # drop rows without labels (MACE) or HF re-hospitalization
    df.dropna(subset = ["Major cardiac events", 'HF re-hospitalization'], inplace=True)
    # separate the participant number in the different dataframe
    df_pnum = df[['participant number']]
    df = df.drop(columns=['participant number'])
    # fix HF re-hospitalization (typo 2 to 1)
    df.loc[df['HF re-hospitalization']==2,'HF re-hospitalization'] = 1
    # fix AF (typo 9 to 0)
    df.loc[df['AF']==9,'AF'] = 0
    # fix NTProBNP when over 35,000 (machine limits)
    df.loc[df['NTProBNP']=='>35,000','NTProBNP'] = 35001
    df.loc[df['NTProBNP']=='> 35000','NTProBNP'] = 35001
    df.loc[df['NTProBNP']=='>35000','NTProBNP'] = 35001
    df['NTProBNP'] = df['NTProBNP'].astype('float')
    # fix LV mass index typo (, to .)
    df.loc[df['LV mass index']=='183,7','LV mass index'] = 183.7
    df['LV mass index'] = df['LV mass index'].astype('float')
    # fix missing data of BMI, BSA, HR with mean values
    df['BMI'] = df['BMI'].fillna(df['BMI'].mean())
    df['BSA'] = df['BSA'].fillna(df['BSA'].mean())
    df['HR'] = df['HR'].fillna(df['HR'].mean().round())
    # Fix LA diameter using formula from https://onlinelibrary.wiley.com/doi/full/10.1111/echo.14943
    # LA diameter = 10.7 + 0.27 * LAVI + 10.6 * BSA
    idx = df['LA diameter'].isnull()
    df.loc[idx, 'LA diameter'] = (10.7 + (0.27 * df['LAVI'][idx]) + (10.6 * df['BSA'][idx])) / 10
    
    if nomiss:
        df['smoke'] = df['smoke'].fillna(0)
        df['stroke'] = df['stroke'].fillna(0)
        # drop missing records
        df.dropna(inplace=True)
    else:
        # fix missing data by filling with 0
        df = df.fillna(0)
    
    if get_patient_no:
        return df, df_pnum
    else:
        return df
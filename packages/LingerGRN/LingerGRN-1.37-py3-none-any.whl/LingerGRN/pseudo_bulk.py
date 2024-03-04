import numpy as np
import pandas as pd
import random
from LingerGRN.immupute_dis import immupute_dis
def tfidf(ATAC):
    O = 1 * (ATAC > 0)
    tf1 = O / (np.ones((O.shape[0], 1)) * np.log(1 + np.sum(O, axis=0))[np.newaxis,:])
    idf = np.log(1 + O.shape[1] / (1 + np.sum(O > 0, axis=1)))
    O1 = tf1 * (idf[:, np.newaxis] * np.ones((1, O.shape[1])))
    O1[np.isnan(O1)] = 0
    RE = O1.T
    return RE
def pseudo_bulk(RNA_file,ATAC_file,label_file,Input_dir):
    RNA=pd.read_csv(Input_dir+RNA_file,sep='\t',index_col=0)
    ATAC=pd.read_csv(Input_dir+ATAC_file,sep='\t',index_col=0)
    RNA = np.log2(1 + RNA)
    from sklearn.impute import KNNImputer
    K=int(np.floor(np.sqrt(RNA.shape[1])))
    imputer = KNNImputer(n_neighbors=K)
# RNA row is genes col is cells
    TG_filter1 = imputer.fit_transform(RNA.values.T)
    TG_filter1=pd.DataFrame(TG_filter1.T,columns=RNA.columns,index=RNA.index)
    RE_filter1 = imputer.fit_transform(np.log2(1+ATAC.values.T))
    RE_filter1=pd.DataFrame(RE_filter1.T,columns=ATAC.columns,index=ATAC.index)
    label=pd.read_csv(Input_dir+label_file,header=None)
    label.columns=['label']
    label.index=RNA.columns
    #label=label['label'].values
    cluster=list(set(label['label'].values))
    allindex=[]
    np.random.seed(42)  # Set seed for reproducibility
    for i in range(len(cluster)):
        temp=label[label['label']==cluster[i]].index
        N = len(temp) # Total number of elements
        m = int(np.floor(np.sqrt(N)))+1  # Number of elements to sample
        sampled_elements = random.sample(range(N), m)
        temp=temp[sampled_elements]
        allindex=allindex+temp.tolist()
    TG_psedubulk = TG_filter1[allindex]
    RE_psedubulk = RE_filter1[allindex]
    return TG_psedubulk,RE_psedubulk
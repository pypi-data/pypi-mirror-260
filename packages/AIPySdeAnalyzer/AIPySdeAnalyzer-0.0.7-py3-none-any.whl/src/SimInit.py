import numpy as np
import os
import pandas as pd
import pymc as pm
import matplotlib.pyplot as plt
import seaborn as sns
import tqdm as tqdm


RANDOM_SEED = 8927
rng = np.random.default_rng(RANDOM_SEED)

import random


class SimInit:
    """
    Manages initiation of simulations based on user-defined parameters.

    This class serves as the starting point for simulations, taking user-specified parameters
    and saving them into an HDF5 (.h5) file for persistent storage. It acts as a base class,
    passing the initialized parameters to inherited classes responsible for executing
    the actual simulation tasks.

    Parameters are encapsulated in an HDF5 file due to its efficiency in handling large
    datasets and its hierarchical structure, which is suitable for complex simulations.

    The class is designed to be inherited by specific simulation classes, which will
    implement the detailed logic necessary for performing the simulation based on the
    initial parameters.
    
    parameters
    ==========
    targetNum: int
    geneNum: int
    effectSgRNA: int, 
        between 0 to 5
    
    return
    ======
    dfSubset: table
    effective_sgRNA_flat: list
    
    """
    def __init__(self,targetNum,geneNum,effectSgRNA):
        self.targetNum = targetNum
        self.geneNum = geneNum
        self.effectSgRNA = effectSgRNA
        self.dfSubset,self.effective_sgRNA_flat = self.loading_data()

    def loading_data(self):
        if self.geneNum is None or self.targetNum is None or self.targetNum > self.geneNum or self.targetNum==0:
            raise ValueError("Invalid or missing parameters. Please ensure targetNum is not 0, parameters are not None, and targetNum is less than or equal to geneNum.") 
        else:
            file_path = 'datasgRNA.h5'
            data_key = 'dataset' 
            dfinit = pd.read_hdf(file_path, key=data_key)
            df = dfinit.iloc[8:,:]
            unique_genes = df['gene'].unique()
            selected_genes = random.sample(list(unique_genes), self.geneNum)  # Randomly select
            dfSubset = df[df['gene'].isin(selected_genes)]
            target_genepool = random.sample(list(selected_genes), self.targetNum)
            effective_sgRNA = [dfSubset.loc[dfSubset['gene'] == gene,'sgID'].to_list()[0:self.effectSgRNA] for gene in set(target_genepool)]
            effective_sgRNA_flat = [item for sublist in effective_sgRNA for item in sublist]
            return dfSubset, effective_sgRNA_flat
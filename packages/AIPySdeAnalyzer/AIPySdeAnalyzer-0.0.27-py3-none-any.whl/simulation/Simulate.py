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
from aipysanalyser.SimInit import SimInit


class Simulate(SimInit):
    """
    Initialize the simulation module inheriting the starting dataset with preset target sgRNAs.
    During the simulation, a master plasmid table (df.M) is generated using a negative binomial 
    distribution. The H_0 sample (representing conditions before screening) is generated from 
    a multinomial distribution with known confounding parameters. H_1 (post-screen sample) 
    is generated from H_1 by selecting target hits with some residual noise introduced by the user.

    Parameters
    ----------
    tpRatio : int
        The target plasmid ratio, indicating the balance between target and control.
    n : int
        Expected negative binomial rate (mu) for the distribution.
    p : float
        Dispersion (alpha) of the negative binomial distribution.
    size : int
        The total sum of the master (M) sample before generating H_0.
    FalseLimits : tuple of float
        A tuple indicating the minimum and maximum viral particles per cell. e.g. (0.01,0.5)
    ObservationNum : int
        The number of observations to generate. fov of vie e.g. 70 cells per fov with sd of 3
    *args
        Variable length argument list for parent class initialization.
    **kwargs
        Arbitrary keyword arguments for parent class initialization.

    Returns
    -------
    dfSim : DataFrame
        Simulated DataFrame, representing H_0 sample before selection.
    df_M : DataFrame
        Master plasmid DataFrame, generated from a negative binomial distribution.
    Original : DataFrame
        Original H_0 DataFrame before the screening process.
    dfQ1 : DataFrame
        DataFrame of all the non-selected targets.
    dfQ2 : DataFrame
        Target DataFrame, indicating selected hits post-screening.
    """
    def __init__(self, tpRatio,n, p,low,high, size,FalseLimits, ObservationNum, *args, **kwargs):
        self.tpRatio = tpRatio
        self.n = n #mu
        self.p = p #alpha
        self.low = low,
        self.high =high, 
        self.size = size
        self.FalseLimits = FalseLimits
        self.ObservationNum = ObservationNum
        super().__init__(*args, **kwargs)
        self.dfSim,self.df_m = self.observePerRaw()
        
    def observePerRaw(self):
        ''':param
            50_000 observation are compitable with the meory usage
            seed_num intiger from 0 to 2
        '''
        
        df = self.dfSubset
        df['count_sim'] = pm.draw(pm.NegativeBinomial.dist(mu=self.p, alpha=self.n),draws=len(self.dfSubset), random_seed=RANDOM_SEED)
        df['count_sim_p'] = df['count_sim'].values/np.sum(df['count_sim'].values)
        df_m = df.copy()
        np.random.seed(123124)
        sgRNA = df['sgID'].values
        MOI = np.random.randint(self.low, self.high, self.size)  # control MOI levels
        # MOI metrix
        seed_random = random.randint(10000, 99999) # seed generated from random module
        MOI_mat = pm.draw(pm.Multinomial.dist(n = MOI,p = df['count_sim_p'].values),draws=1, random_seed=seed_random)
        # Assign 1 the hits above 1
        MOI_mat = np.where(MOI_mat > 1, 1, MOI_mat)
        # Replace ones with corresponding sgRNA from map and assign activity
        Qoriginal = {}
        progress = tqdm.tqdm()
        print("generates ht0 sample")
        for i,row in enumerate(MOI_mat):
            temp_sgRNA = ['#'.join(filter(None, (sgRNA[col] if val==1 else '' for col, val in enumerate(row))))]
            activity = [any(word in sg for word in self.effective_sgRNA_flat) for sg in temp_sgRNA]
            Qoriginal[i] = temp_sgRNA + activity
            progress.update()
        df = pd.DataFrame.from_dict(Qoriginal, orient='index', columns=['sgID', 'Active'])
        df.reset_index(level=0, inplace=True)
        df.rename(columns = {'index':'cell'}, inplace = True)
        table = df.sample(frac=1, replace=False, random_state=1564743454, axis=0, ignore_index=True)
        return table,df_m

    def simulation(self):
        '''
        :param FalseLimits, tuple, precantage list of False Positive
        :param ObservationNum, tuple, mean and standard deviation
        '''
        Original = self.dfSim
        dfQ1 = {}
        dfQ2 = {}
        fpRate = [arr for arr in np.arange(self.FalseLimits[0], self.FalseLimits[1], self.FalseLimits[0])]
        progress = tqdm.tqdm()
        while True:
            progress.update()
            FOV = int(np.random.normal(self.ObservationNum[0],self.ObservationNum[1]))
            if FOV > len(self.dfSim):
                break
            dfTemp = self.dfSim.iloc[:FOV,:]
            # shorten the table by fov
            self.dfSim = self.dfSim.iloc[FOV+1:,:]
            idxTruePostive = dfTemp.index[dfTemp['Active']].tolist()
            if len(idxTruePostive) > 0:
                TruePositiveSGs = dfTemp.loc[idxTruePostive, 'sgID'].to_list()
                dfTemp = dfTemp.drop(idxTruePostive)
                for sg in TruePositiveSGs:
                    if sg in dfQ2.keys():
                        dfQ2[sg] += 1
                    else:
                        dfQ2[sg] = 1
            selFP = int(len(dfTemp.index.to_list()) * random.sample(fpRate,1)[0])
            if selFP > 0:
                TruePositiveSGs =  dfTemp['sgID'].sample(n = selFP).to_list()
                for sg in TruePositiveSGs:
                    dfTemp = dfTemp[dfTemp.sgID != sg]
                    if sg in dfQ2.keys():
                        dfQ2[sg] += 1
                    else:
                        dfQ2[sg] = 1
            sgRNAexclude =  dfTemp['sgID'].to_list()
            for sg in sgRNAexclude:
                if sg in dfQ1.keys():
                    dfQ1[sg] += 1
                else:
                    dfQ1[sg] = 1
        df_m = self.df_m.reset_index()
        df_Q1 = pd.DataFrame({"sgID": list(dfQ1.keys()), "Q1_Reads": list(dfQ1.values())}).reset_index()
        df_Q2 = pd.DataFrame({"sgID": list(dfQ2.keys()), "Q2_Reads": list(dfQ2.values())}).reset_index()
        origDict = Original['sgID'].value_counts().to_dict()
        df_orig = pd.DataFrame({'sgRNA':[sgr for sgr in origDict.keys()],'count':[count for count in origDict.values()]}).reset_index()
        print("Data generation is done")
        return df_orig,df_Q1,df_Q2,df_m
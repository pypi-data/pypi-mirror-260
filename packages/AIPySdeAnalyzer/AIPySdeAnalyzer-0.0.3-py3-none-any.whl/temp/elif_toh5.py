import pandas as pd
import os
# Creating a simple DataFrame
path = r"D:\Gil\temp"
df = pd.DataFrame(pd.read_excel(os.path.join(path,"elife-19760-supp3-v2.xlsx"))) 
file_path = 'datasgRNA.h5'
data_key = 'dataset'

df.to_hdf(file_path, key=data_key, mode='w')

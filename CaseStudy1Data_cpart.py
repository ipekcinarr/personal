import numpy as np
import pandas as pd

entrynode = np.arange(1,47,1)
print(entrynode)
exitnode = np.arange(1,47,1)

df_CostMatrix = pd.read_excel(r'C:\Users\Bartu\Desktop\CaseStudy1NewData.xlsx', sheet_name='Sheet1', header=0, skiprows=0,nrows=47,usecols='B:AV')
df_Upper = pd.read_excel(r'C:\Users\Bartu\Desktop\CaseStudy1NewData.xlsx', sheet_name='Sheet3',header=0,index_col=0)
CostMatrix = {}

for i in np.arange(len(entrynode)):
    for j in np.arange(len(exitnode)):
        CostMatrix[(i+1, j+1)] = df_CostMatrix.iloc[i, j]

Upper= {}
Upper= {}
for j in np.arange(len(exitnode)):
    Upper[j+1]=df_Upper.iloc[0,j]

print(CostMatrix)
print(Upper)


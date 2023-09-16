import phenograph
import numpy as np
import pandas as pd
import scanpy as sc
from matplotlib import pyplot as plt


df = pd.read_csv("Levine_13dim.txt", sep='\t')
df = df.drop(['label'], axis=1)
#print(df)
data = df.to_numpy()

communities, graph, Q = phenograph.cluster(data)
print(communities)

sc.pl.umap(
    df,
    color=communities,
    palette='tab20', # 'palette' specifies the colormap to use)
    title=["Clusters"])

from sklearn.decomposition import PCA

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans


pca_dim = 2

# Load Data
data = pd.read_csv("Levine_13dim.txt", sep="\t")
print(data.head())
data = data.dropna()
labels = data['label']
print(labels.shape)
data = data.drop(['label'], axis=1)
print(data.shape)
from sklearn.cluster import DBSCAN

# Transform the data
pca = PCA(pca_dim)
df = pca.fit_transform(data)



# Import KMeans module


# Initialize the class object
kmeans = KMeans(n_clusters=3)
#print(df.shape)
# predict the labels of clusters.
label = kmeans.fit_predict(df)
#print(np.reshape(label, (81747,1)).shape)
# Getting unique labels
u_labels = np.unique(label)
plt.figure('PCA et kmeans')
# plotting the results:
for i in u_labels:
    plt.scatter(df[label == i, 0], df[label == i, 1], label=i, marker=".")
plt.legend()


# Découpage du dataset en sous dataset en fonction des cluster formés par le kmeans
results = np.hstack((data, np.reshape(label, (81747,1))))
data2 = pd.DataFrame(results, columns=['CD45', 'CD45RA', 'CD19', 'CD11b', 'CD4	', 'CD8	', 'CD34', 'CD20', 'CD33', 'CD123', 'CD38', 'CD90', 'CD3', 'label'])
print(data2.head())
data0 = data2[data2['label'] == 0]
data1 = data2[data2['label'] == 1]
data2 = data2[data2['label'] == 2]
print(data0.shape)
print(data1.shape)
print(data2.shape)
#########


labels = data0['label']
print(labels.shape)
data0 = data0.drop(['label'], axis=1)
print(data0.shape)


# Transform the data
pca = PCA(pca_dim)
df = pca.fit_transform(data0)

# Initialize the class object
kmeans = KMeans(n_clusters=3)
#print(df.shape)
# predict the labels of clusters.
label = kmeans.fit_predict(df)
#print(np.reshape(label, (81747,1)).shape)
# Getting unique labels
u_labels = np.unique(label)
plt.figure('PCA et kmeans 2')
# plotting the results:
for i in u_labels:
    plt.scatter(df[label == i, 0], df[label == i, 1], label=i, marker=".")
plt.legend()



data = pd.read_csv("Levine_13dim.txt", sep="\t")
data = data.dropna()
labels = data['label']
data = data.drop(['label'], axis=1)
data = data.dropna()
pca = PCA(pca_dim)
#print(type(labels))
# Transform the data
df = pca.fit_transform(data)
data = pd.read_csv("Levine_13dim.txt", sep="\t")
data = data.dropna()
print('labels = ', data['label'].shape)
#print(df.shape)
plt.figure('PCA et labels')
plt.scatter(df[:, 0], df[:, 1],
    # colorer en utilisant la variable 'Rank'
    c=data.get('label'), marker=".")

plt.colorbar()
plt.show()
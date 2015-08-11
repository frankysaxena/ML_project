import getting_features
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.mlab import PCA
from numpy import *

import matplotlib.pyplot as plt

from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn import decomposition
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import Imputer

random_data = np.loadtxt("random_sample.dat", unpack=True)

X = np.array(random_data).all()
y = np.array(random_data).all()

# print banned_data
pca = PCA(n_components=2)
X_r = pca.fit(random_data).transform(random_data)
print X_r
plt.figure()
plt.scatter(X_r[:,  0], X_r[:, 1])
plt.title('PCA of dataset')
plt.show()

#
# np.random.seed(5)
#
# centers = [[1, 1], [-1, -1], [1, -1]]
# features = datasets.x()
# X = features.data
# y = features.target
#
# fig = plt.figure(1, figsize=(4, 3))
# plt.clf()
# ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
#
# plt.cla()
# pca = decomposition.PCA(n_components=3)
# pca.fit(X)
# X = pca.transform(X)
# #
# # for name, label in [('Setosa', 0), ('Versicolour', 1), ('Virginica', 2)]:
# #     ax.text3D(X[y == label, 0].mean(),
# #               X[y == label, 1].mean() + 1.5,
# #               X[y == label, 2].mean(), name,
# #               horizontalalignment='center',
# #               bbox=dict(alpha=.5, edgecolor='w', facecolor='w'))
# # Reorder the labels to have colors matching the cluster results
# y = np.choose(y, [1, 2, 0]).astype(np.float)
# ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=y, cmap=plt.cm.spectral)
#
# x_surf = [X[:, 0].min(), X[:, 0].max(),
#           X[:, 0].min(), X[:, 0].max()]
# y_surf = [X[:, 0].max(), X[:, 0].max(),
#           X[:, 0].min(), X[:, 0].min()]
# x_surf = np.array(x_surf)
# y_surf = np.array(y_surf)
# v0 = pca.transform(pca.components_[0])
# v0 /= v0[-1]
# v1 = pca.transform(pca.components_[1])
# v1 /= v1[-1]
#
# ax.w_xaxis.set_ticklabels([])
# ax.w_yaxis.set_ticklabels([])
# ax.w_zaxis.set_ticklabels([])
#
# plt.show()

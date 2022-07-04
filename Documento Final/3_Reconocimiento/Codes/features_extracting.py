from sklearn.decomposition import KernelPCA
from sklearn.naive_bayes import GaussianNB

kpcaModel = KernelPCA(n_components=16)  # KPCA for dimensionality reduction
gnbClassifier = GaussianNB()  # Gaussian naive Bayes classifier

X = np.array(X)  # Convert training features vector to numpy array
y = np.array(y)  # Convert training samples labels to numpy array

# -------- DIMENSIONALITY REDUCTION BY KERNEL PCA --------- #
# Fits the model and apply transformation to the features vector
X = kpcaModel.fit_transform(X, y)
# ---------- FITS THE CLASSIFIER ----------#
gnbClassifier.fit(X, y)
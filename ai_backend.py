import numpy as np
import mne
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

###NOTE: function not complete, finish later###
def edf_to_datafile(filepath, supervised):
    """Helper function that will convert the .edf file into a datafile that can be used for ML.
    
    This function should be implemented to read the .edf file and return (X, y) for supervised learning
    or X for unsupervised learning. For now, it returns dummy data as a placeholder.
    
    Parameters:
    filepath (str): Path to the .edf file.
    
    Returns:
    tuple or array-like: (X, y) for supervised learning or X for unsupervised learning.
    """
    #Read edf contents
    data = mne.io.read_raw_edf(filepath)
    X = data.get_data()
    y = data.ch_names()

    if supervised:
        return X, y
    else:
        return X

def linear_discriminant_analysis(datafile, solver, shrinkage, n_components):
    """Trains an LDA model on the provided datafile.
    
    Parameters:
    datafile (tuple): A tuple (X, y) where X is the feature matrix and y is the label vector.
    solver (str): Solver to use ('svd', 'lsqr', 'eigen').
    shrinkage (str or float): Shrinkage parameter for 'lsqr' and 'eigen' solvers.
    n_components (int or None): Number of components for dimensionality reduction.
    
    Returns:
    LinearDiscriminantAnalysis: The trained LDA model.
    """
    X, y = datafile
    model = LinearDiscriminantAnalysis(solver=solver, shrinkage=shrinkage, n_components=n_components)
    model.fit(X, y)
    return model

def support_vector_machine(datafile, kernel, c, gamma):
    """Trains an SVM model on the provided datafile.
    
    Parameters:
    datafile (tuple): A tuple (X, y) where X is the feature matrix and y is the label vector.
    kernel (str): Type of kernel function ('linear', 'poly', 'rbf', 'sigmoid').
    c (float): Regularization parameter.
    gamma (str or float): Kernel coefficient for 'rbf', 'poly', and 'sigmoid'.
    
    Returns:
    SVC: The trained SVM model.
    """
    X, y = datafile
    model = svm.SVC(kernel=kernel, C=c, gamma=gamma)
    model.fit(X, y)
    return model

def random_forest(datafile, n_estimators, max_depth, min_samples_split, min_samples_leaf, max_features):
    """Trains a Random Forest model on the provided datafile.
    
    Parameters:
    datafile (tuple): A tuple (X, y) where X is the feature matrix and y is the label vector.
    n_estimators (int): Number of trees in the forest.
    max_depth (int or None): Maximum depth of the tree.
    min_samples_split (int): Minimum number of samples required to split an internal node.
    min_samples_leaf (int): Minimum number of samples required at a leaf node.
    max_features (str or int): Number of features to consider for the best split.
    
    Returns:
    RandomForestClassifier: The trained Random Forest model.
    """
    X, y = datafile
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth,
                                   min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf,
                                   max_features=max_features)
    model.fit(X, y)
    return model

def gradient_boosting_machine(datafile, n_estimators, learning_rate, max_depth, min_samples_split, subsample):
    """Trains a Gradient Boosting Machine model on the provided datafile.
    
    Parameters:
    datafile (tuple): A tuple (X, y) where X is the feature matrix and y is the label vector.
    n_estimators (int): Number of boosting stages.
    learning_rate (float): Learning rate shrinks the contribution of each tree.
    max_depth (int): Maximum depth of the individual trees.
    min_samples_split (int): Minimum number of samples required to split an internal node.
    subsample (float): Fraction of samples used for fitting the trees.
    
    Returns:
    GradientBoostingClassifier: The trained GBM model.
    """
    X, y = datafile
    model = GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=learning_rate,
                                       max_depth=max_depth, min_samples_split=min_samples_split,
                                       subsample=subsample)
    model.fit(X, y)
    return model

def k_means_clustering(datafile, n_clusters, init):
    """Trains a K-means clustering model on the provided datafile.
    
    Parameters:
    datafile (array-like): The feature matrix X.
    n_clusters (int): Number of clusters.
    init (str): Initialization method ('k-means++', 'random').
    
    Returns:
    KMeans: The trained K-means model.
    """
    X = datafile
    model = KMeans(n_clusters=n_clusters, init=init)
    model.fit(X)
    return model

def gaussian_mixture_model(datafile, n_components, covariance_type):
    """Trains a Gaussian Mixture Model on the provided datafile.
    
    Parameters:
    datafile (array-like): The feature matrix X.
    n_components (int): Number of mixture components.
    covariance_type (str): Type of covariance parameters ('full', 'tied', 'diag', 'spherical').
    
    Returns:
    GaussianMixture: The trained GMM model.
    """
    X = datafile
    model = GaussianMixture(n_components=n_components, covariance_type=covariance_type)
    model.fit(X)
    return model
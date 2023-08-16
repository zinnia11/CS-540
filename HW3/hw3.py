from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt

def load_and_center_dataset(filename):
    X = np.load(filename) # numpy array, should be dimensions 2414x1024
    # center by subtracting mean
    X = X - np.mean(X, axis=0)
    return X
    pass

def get_covariance(dataset):
    XT = np.transpose(dataset)
    return np.dot(XT, dataset) / (len(dataset)-1) # covariance matrix X, should be dimensions 1024x1024
    pass

def get_eig(S, m):
    values, vectors = eigh(S, subset_by_index=[len(S)-m, len(S)-1]) # only want to largest m 
    vectors = np.fliplr(vectors) # flip the columns, which each represent a eigenvector
    # values in descending diagonal matrix
    values = np.flip(values) 
    values = np.diag(values) 
    return values, vectors
    pass

def get_eig_prop(S, prop):
    # calculate the total of all the eigenvalues
    allvec = eigh(S, eigvals_only=True)
    allvec = np.diag(allvec)
    total = np.trace(allvec)
    # find the eigenvalue that has the given proportion of variance
    prop = prop * total
    # find the eigenvalues and vectors with a greater proportion of variance and return
    values, vectors = eigh(S, subset_by_value=[prop, np.inf])
    vectors = np.fliplr(vectors) 
    values = np.flip(values) 
    values = np.diag(values) 
    return values, vectors
    pass

def project_image(image, U):
    # Your implementation goes here!
    U = np.transpose(U) # every row is now a eigenvector
    A = np.dot(U, image)
    A = np.dot(A, U)
    return np.reshape(A, -1)
    pass

def display_image(orig, proj):
    # Your implementation goes here!
    orig = np.reshape(orig, (32,32), 'F')
    proj = np.reshape(proj, (32,32), 'F')

    fig, (axs_o, axs_p) = plt.subplots(1, 2)

    axs_o.set_title('Original')
    i_orig = axs_o.imshow(orig, aspect='equal')
    fig.colorbar(i_orig, ax=axs_o)

    axs_p.set_title('Projection')
    i_proj = axs_p.imshow(proj, aspect='equal')
    fig.colorbar(i_proj, ax=axs_p)

    plt.show()
    pass



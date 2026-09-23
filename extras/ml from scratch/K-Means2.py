import numpy as np
from scipy.cluster.hierarchy import centroid


class KMeans:
    """
        K-Means clustering algorithm implementation.

        Parameters:
            K (int): Number of clusters

        Attributes:
            K (int): Number of clusters
            centroids (numpy.ndarray): Array containing the centroids of each cluster

        Methods:
            __init__(self, K): Initializes the Kmeans instance with the specified number of clusters.
            initialize_centroids(self, X): Initializes the centroids for each cluster by selecting K random points from the dataset.
            assign_points_centroids(self, X): Assigns each point in the dataset to the nearest centroid.
            compute_mean(self, X, points): Computes the mean of the points assigned to each centroid.
            fit(self, X, iterations=10): Clusters the dataset using the K-Means algorithm.
        """
    def __init__(self, K):
        assert K > 0, "K should be a positive integer"
        self.K = K

    def initialize_centoids(self, X):
        assert X.shape[0] >= self.K, "Number of data points should be greater than or equal to K."

        randomized_X = np.random.permutation(X.shape[0]) # Bir tam sayı verirsen (n)Bu durumda 0 ile n-1 arasındaki sayıları karıştırıp sana döner:
        centroid_idx = randomized_X[:self.K] # get the indices for the centroids (ilk K sayıyı al)
        self.centroids = X[centroid_idx] # asssign the centroids to the selected points

    def assign_points_centroids(self, X):
        """
                Assign each point in the dataset to the nearest centroid.

                Parameters:
                X (numpy.ndarray): dataset to cluster

                Returns:
                numpy.ndarray: array containing the index of the centroid for each point
                """
        X = np.expand_dims(X, axis=1)
        distance = np.linalg.norm(X - self.centroids, axis=-1) #calculate Euclidean distance between each point and each centroid
        points = np.argmin(distance, axis=1) # assign each point to the closest centroid
        assert len(points) == X.shape[0], "Number of assigned points should equal the number of data points"
        return points

    def compute_mean(self, X, points):
        """
                Compute the mean of the points assigned to each centroid.

                Parameters:
                X (numpy.ndarray): dataset to cluster
                points (numpy.ndarray): array containing the index of the centroid for each point

                Returns:
                numpy.ndarray: array containing the new centroids for each cluster
                """
        centroids = np.zeros((self.K, X.shape[1]))
        for i in range(self.K):
            centroid_mean = X[points == i].mean(axis=0) # calculate mean of the poitns assigned to the current centroid
            centroids[i] = centroid_mean

        return centroids

    def fit(self, X, iterations=10):
        """
                Cluster the dataset using the K-Means algorithm.

                Parameters:
                X (numpy.ndarray): dataset to cluster
                iterations (int): number of iterations to perform (default=10)

                Returns:
                numpy.ndarray: array containing the final centroids for each cluster
                numpy.ndarray: array containing the index of the centroid for each point
                """
        self.initialize_centoids(X)
        for i in range(iterations):
            points = self.assign_points_centroids(X)
            self.centroids = self.compute_mean(X, points)

            # Assertions for debugging and validation
            assert len(self.centroids) == self.K, "Number of centroids should equal K."
            assert X.shape[1] == self.centroids.shape[1], "Dimensionality of centroids should match input data."
            assert max(points) < self.K, "Cluster index should be less than K."
            assert min(points) >= 0, "Cluster index should be non-negative."

        return self.centroids, points
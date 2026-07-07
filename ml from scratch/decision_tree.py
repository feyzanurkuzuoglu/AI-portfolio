import numpy as np


class Node():
    def __init__(self, feature=None, threshold=None, left=None, right=None, gain=None, value=None):
        """
                Initializes a new instance of the Node class.

                Args:
                    feature: The feature used for splitting at this node. Defaults to None.
                    threshold: The threshold used for splitting at this node. Defaults to None.
                    left: The left child node. Defaults to None.
                    right: The right child node. Defaults to None.
                    gain: The gain of the split. Defaults to None.
                    value: If this node is a leaf node, this attribute represents the predicted value
                        for the target variable. Defaults to None.
                """
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.gain = gain
        self.value = value

class DecisionTree():
    def __init__(self, min_samples=2, max_depth=2):
        """Constructor for DecisionTree class. """

    def split_data(self, dataset, feature, threshold):
        """
                Splits the given dataset into two datasets based on the given feature and threshold.

                Parameters:
                    dataset (ndarray): Input dataset.
                    feature (int): Index of the feature to be split on.
                    threshold (float): Threshold value to split the feature on.

                Returns:
                    left_dataset (ndarray): Subset of the dataset with values less than or equal to the threshold.
                    right_dataset (ndarray): Subset of the dataset with values greater than the threshold.
                """
        left_dataset = []
        right_dataset = []

        for row in dataset:
            if row[feature] <= threshold:
                left_dataset.append(row)
            else:
                right_dataset.append(row)

        left_dataset = np.array(left_dataset)
        right_dataset = np.array(right_dataset)

        return left_dataset, right_dataset


    def entropy(self, y):
        """
                Computes the entropy of the given label values.

                Parameters:
                    y (ndarray): Input label values.

                Returns:
                    entropy (float): Entropy of the given label values.
                """
        entropy = 0
        labels = np.unique(y)

        for label in labels:
            # find the examples in y that have the current label
            label_examples = y[y==label]
            # calculate the ratio of the current label in y
            p1 = len(label_examples) / len(y)
            # calculate the entropy using the current label and ratio
            entropy += -p1 * np.log2(p1)

        return entropy

    def information_gain(self, parent, left, right):
        """
                Computes the information gain from splitting the parent dataset into two datasets.

                Parameters:
                    parent (ndarray): Input parent dataset.
                    left (ndarray): Subset of the parent dataset after split on a feature.
                    right (ndarray): Subset of the parent dataset after split on a feature.

                Returns:
                    information_gain (float): Information gain of the split.
                """
        information_gain = 0
        parent_entropy = self.entropy(parent)
        weight_left = len(left) / len(parent)
        weight_right = len(right) / len(parent)
        entropy_left, entropy_right = self.entropy(left), self.entropy(right)
        weighted_entropy = weight_left*entropy_left + weight_right*entropy_right
        information_gain = parent_entropy - weighted_entropy

        return information_gain

    def best_split(self, dataset, num_samples, num_features):
        """
                Finds the best split for the given dataset.

                Args:
                dataset (ndarray): The dataset to split.
                num_samples (int): The number of samples in the dataset.
                num_features (int): The number of features in the dataset.

                Returns:
                dict: A dictionary with the best split feature index, threshold, gain,
                      left and right datasets.
                """
        # dictionary to store the best split values
        best_split = {"gain":-1, "feature":None, "threshold":None}
        for feature_index in range(num_features):
            #get the feature at the current feature_index
            feature_values = dataset[:, feature_index]
            thresholds = np.unique(feature_values),
            for threshold in thresholds:
                left_dataset, right_dataset = self.split_data(dataset, feature_index, threshold)
                # check if either datasets is empty
                if len(left_dataset) and len(right_dataset):
                    y, left_y, right_y = dataset[:, -1], left_dataset[:, -1], right_dataset[:, -1]
                    information_gain = self.information_gain(y, left_y, right_y)
                    # update the best split if coniditons are met
                    if information_gain > best_split["gain"]:
                        best_split["feature"] = feature_index
                        best_split["threshold"] = threshold
                        best_split["left_dataset"] = left_dataset
                        best_split["right_dataset"] = right_dataset
                        best_split["gain"] = information_gain

        return best_split

    def calculate_leaf_value(self, y):
        """
                Calculates the most occurring value in the given list of y values.

                Args:
                    y (list): The list of y values.

                Returns:
                    The most occurring value in the list.
                """

        y = list(y)
        #get the highest present class in the array
        most_occuring_value = max(y, key=y.count)
        return most_occuring_value

    def built_tree(self, dataset, current_depth=0):
        """
                Recursively builds a decision tree from the given dataset.

                Args:
                dataset (ndarray): The dataset to build the tree from.
                current_depth (int): The current depth of the tree.

                Returns:
                Node: The root node of the built decision tree.
                """
        # split the dataset into X, y values
        X, y = dataset[:, :-1], dataset[:, -1]
        n_samples, n_features = X.shape
        #keeps splitting until stopping conditions are met
        if n_samples >= self.min_samples and current_depth <= self.max_depth:
            best_split = self.best_split(dataset, n_samples, n_features)
            #check if the gain isn't zero
            if best_split["gain"]:
                #continue splitting the left and right child. increment current depth
                left_node = self.built_tree(best_split["left_dataset"], current_depth+1)
                right_node = self.built_tree(best_split["right_dataset"], current_depth+1)

                return Node(best_split["feature"], best_split["threshold"], left_node, right_node, best_split["gain"])

        # compute leaf node value
        leaf_value = self.calculate_leaf_value(y)
        return Node(value=leaf_value)

    def fit(self, X, y):
        """
                Builds and fits the decision tree to the given X and y values.

                Args:
                X (ndarray): The feature matrix.
                y (ndarray): The target values.
                """
        dataset = np.concatenate((X,y), axis=1)
        self.root = self.built_tree(dataset)

    def predict(self, X):
        """
                Predicts the class labels for each instance in the feature matrix X.

                Args:
                X (ndarray): The feature matrix to make predictions for.

                Returns:
                list: A list of predicted class labels.
                """
        predictions = []
        # for each instance in X make a prediction by transversing the tree
        for x in X:
            prediction = self.make_prediction(x, self.root)
            predictions.append(prediction)
        np.array(predictions)
        return predictions

    def make_prediction(self, x, node):
        """
                Traverses the decision tree to predict the target value for the given feature vector.

                Args:
                x (ndarray): The feature vector to predict the target value for.
                node (Node): The current node being evaluated.

                Returns:
                The predicted target value for the given feature vector.
                """
        # if the node has value i.e it's a leaf node extract it's value
        if node.value != None:
            return node.value
        else:
            # if it's node a leaf node we'll get it's feature and traverse through the tree accordingly
            feature = x[node.feature]
            if feature <= node.threshold:
                return self.make_prediction(x, node.left)
            else:
                return self.make_prediction(x, node.right)


"""EVALUATION"""

def train_test_split(X, y, random_state=42, test_size=0.2):
    """
        Splits the data into training and testing sets.

        Parameters:
            X (numpy.ndarray): Features array of shape (n_samples, n_features).
            y (numpy.ndarray): Target array of shape (n_samples,).
            random_state (int): Seed for the random number generator. Default is 42.
            test_size (float): Proportion of samples to include in the test set. Default is 0.2.

        Returns:
            Tuple[numpy.ndarray]: A tuple containing X_train, X_test, y_train, y_test.
        """
    n_samples = X.shape[0]

    np.random.seed(random_state)
    shuffled_indices = np.random.permutation(np.arange(n_samples))

    test_size = int(n_samples * test_size)

    test_indices = shuffled_indices[:, test_size]
    train_indices = shuffled_indices[test_size, :]

    X_train, X_test = X[train_indices], X[test_indices]
    y_train, y_test = y[train_indices], y[test_indices]

    return X_train, X_test, y_train, y_test

def accuracy(y_true, y_pred):
    """
        Computes the accuracy of a classification model.

        Parameters:
        ----------
            y_true (numpy array): A numpy array of true labels for each data point.
            y_pred (numpy array): A numpy array of predicted labels for each data point.

        Returns:
        ----------
            float: The accuracy of the model
        """
    y_true = y_true.flatten()
    total_samples  =len(y_true)
    correct_predictions = np.sum(y_true == y_pred)
    return (correct_predictions / total_samples)

def balanced_accuracy(y_true, y_pred):
    """Calculate the balanced accuracy for a multi-class classification problem.

        Parameters
        ----------
            y_true (numpy array): A numpy array of true labels for each data point.
            y_pred (numpy array): A numpy array of predicted labels for each data point.

        Returns
        -------
            balanced_acc : The balanced accuracy of the model

        """
    y_pred = np.array(y_pred)
    y_true = y_true.flatten()
    n_classes = len(np.unique(y_true))

    # Initialize an array to store the sensitivity and specificity for each class
    sen = []
    spec = []
    for i in range(n_classes):
        #create a mask for the true and predicted values for class i
        mask_true = y_true == 1
        mask_pred = y_pred == 1

        TP = np.sum(mask_true & mask_pred)
        TN = np.sum((mask_true != True) & (mask_pred != True))
        FP = np.sum((mask_true != True) & mask_pred)
        FN = np.sum(mask_true & (mask_pred != True))

        sensitivity = TP / (TP + FN)
        specifity = TN / (TN + FP)

        sen.append(sensitivity)
        spec.append(specifity)

    average_sen = np.mean(sen)
    average_spec = np.mean(spec)
    balanced_acc = (average_sen + average_spec) / n_classes

    return balanced_acc


class RandomForest:
    """
    A random forest classifier.

    Parameters
    ----------
    n_trees : int, default=7
        The number of trees in the random forest.
    max_depth : int, default=7
        The maximum depth of each decision tree in the random forest.
    min_samples : int, default=2
        The minimum number of samples required to split an internal node
        of each decision tree in the random forest.

    Attributes
    ----------
    n_trees : int
        The number of trees in the random forest.
    max_depth : int
        The maximum depth of each decision tree in the random forest.
    min_samples : int
        The minimum number of samples required to split an internal node
        of each decision tree in the random forest.
    trees : list of DecisionTreeClassifier
        The decision trees in the random forest.
    """
    def __init__(self, n_trees=7, max_depth=7, min_samples=2):
        """
                Initialize the random forest classifier.

                Parameters
                ----------
                n_trees : int, default=7
                    The number of trees in the random forest.
                max_depth : int, default=7
                    The maximum depth of each decision tree in the random forest.
                min_samples : int, default=2
                    The minimum number of samples required to split an internal node
                    of each decision tree in the random forest.
                """
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_samples = min_samples
        self.trees = []

    def fit(self, X, y):
        """
            Build a random forest classifier from the training set (X, y).

            Parameters
            ----------
            X : array-like of shape (n_samples, n_features)
                The training input samples.
            y : array-like of shape (n_samples,)
                The target values.

            Returns
            -------
            self : object
                Returns self.
            """
        self.trees = []
        dataset = np.concatenate((X, y.reshape(-1,1)), axis=1)
        for _ in range(self.n_trees):
            tree = DecisionTree(max_depth=self.max_depth, min_samples=self.min_samples)
            dataset_sample = self.bootstrap_samples(dataset)
            X_sample, y_sample = dataset_sample[:, :-1], dataset_sample[:, -1]
            tree.fit(X_sample, y_sample)
            self.trees.append(tree)

        return self

    def bootstrap_samples(self, dataset):
        """
                Bootstrap the dataset by sampling from it with replacement.

                Parameters
                ----------
                dataset : array-like of shape (n_samples, n_features + 1)
                    The dataset to bootstrap.

                Returns
                -------
                dataset_sample : array-like of shape (n_samples, n_features + 1)
                    The bootstrapped dataset sample.
                """
        n_samples = dataset.shape[0]

        # Generate random indices to index into the dataset with replacement.
        np.random.seed(1)
        indices = np.random.choice(n_samples, n_samples, replace=True)
        dataset_sample = dataset[indices]

        return dataset_sample

    def most_common_label(self, y):
        """
        Return the most common label in an array of labels.

        Parameters
        ----------
        y : array-like of shape (n_samples,)
            The array of labels.

        Returns
        -------
        most_occuring_value : int or float
            The most common label in the array.
        """
        y = list(y)
        # get the highest present class in the array
        most_occuring_value = max(y, key=y.count)
        return most_occuring_value

    def predict(self, X):
        """
        Predict class for X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        majority_predictions : array-like of shape (n_samples,)
            The predicted classes.
        """
        # get prediction from each tree in the tree list on the test data
        predictions = np.array([tree.predict(X) for tree in self.trees])
        # get prediction for the same sample from all trees for each sample in the test data
        preds = np.swapaxes(predictions, 0, 1)
        # get the most voted value by the trees and store it in the final predictions array
        majority_predictions = np.array([self.most_common_label(pred) for pred in preds])
        return majority_predictions
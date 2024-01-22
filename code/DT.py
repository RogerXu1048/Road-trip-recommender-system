import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# define a class for the node
class Node():
    def __init__(self, feature_index=None, threshold=None, left=None, right=None, info_gain=None, value=None):
        # if the node is a decision node
        self.feature_index = feature_index
        self.threshold = threshold
        self.left = left
        self.right = right
        self.info_gain = info_gain

        # if the node is a leaf node
        self.value = value
# define a class for the decision tree (classifier)
class DecisionTree():
    def __init__(self, max_depth=None):
        self.root = None
        # stop when reach the maximum depth
        self.max_depth = max_depth

    def build_tree(self, dataset, curr_depth=0):
        #X are features, Y are labels
        X, Y = dataset[:,:-1], dataset[:,-1]
        #number of rows is number of samples, number of columns is number of features
        num_samples, num_features = np.shape(X)

        # split until reach the maximum depth
        if curr_depth<=self.max_depth:
            # find the best split
            best_split = self.get_best_split(dataset, num_samples, num_features)
            # check if information gain is positive. If it's zero, no need to split
            if best_split["info_gain"]>0:
                # recursion to build left and right trees
                left_subtree = self.build_tree(best_split["dataset_left"], curr_depth+1)
                right_subtree = self.build_tree(best_split["dataset_right"], curr_depth+1)
                # return the decision node
                return Node(best_split["feature_index"], best_split["threshold"],
                            left_subtree, right_subtree, best_split["info_gain"])


        # if reach maximum depth, compute leaf value and return it
        # Leaf value is the most frequent occurring element in the leaf
        unique_values, counts = np.unique(Y, return_counts=True)
        leaf_value = unique_values[np.argmax(counts)]
        return Node(value=leaf_value)

    #best split returns a dictionary to store the info about the best split
    def get_best_split(self, dataset, num_samples, num_features):
        best_split = {}
        #initialize information gain to negative infinity
        max_info_gain = -float("inf")
        best_split["info_gain"] = max_info_gain

        # loop over all the features (the themes in the roadtrip)
        for feature_index in range(num_features):
            feature_values = dataset[:, feature_index]
            #possible thresholds are all the feature values present in the dataset
            possible_thresholds = np.unique(feature_values)
            # loop over all the feature values
            for threshold in possible_thresholds:
                dataset_left = np.empty((0, dataset.shape[1]))
                dataset_right = np.empty((0, dataset.shape[1]))
                # Loop through each row in the dataset
                for row in range(num_samples):
                    #split based on the threshold
                    if dataset[row,feature_index] <= threshold:
                        dataset_left = np.vstack((dataset_left, dataset[row,:]))
                    else:
                        dataset_right = np.vstack((dataset_right, dataset[row,:]))

                if len(dataset_left)>0 and len(dataset_right)>0:
                    parent_labels, left_child_labels, right_child_labels = dataset[:,-1], dataset_left[:,-1], dataset_right[:,-1]
                    # calculate information gain
                    curr_info_gain = self.information_gain(parent_labels, left_child_labels, right_child_labels)
                    # update the best split if greater than the max info gain so far
                    if curr_info_gain>max_info_gain:
                        best_split["feature_index"] = feature_index
                        best_split["threshold"] = threshold
                        best_split["dataset_left"] = dataset_left
                        best_split["dataset_right"] = dataset_right
                        best_split["info_gain"] = curr_info_gain
                        max_info_gain = curr_info_gain

        # return best split
        return best_split

    #calculate information gain for a split by calculating Gini index
    #the higher the better for the split
    def information_gain(self, parent, l_child, r_child):
        weight_l = len(l_child) / len(parent)
        weight_r = len(r_child) / len(parent)
        gain = self.gini_index(parent) - (weight_l*self.gini_index(l_child) + weight_r*self.gini_index(r_child))
        return gain

    #calculate Gini index that measures impurity of dataset. 0 means pure data (all classes are same)
    # the lower the better for the split
    def gini_index(self, y):
        class_labels = np.unique(y)
        gini = 0
        for cls in class_labels:
            #probability of a class in the dataset
            probability_cls = len(y[y == cls]) / len(y)
            gini += probability_cls**2
        return 1 - gini

    def print_tree(self, tree=None, indent=" "):
        if not tree:
            tree = self.root

        if tree.value is not None:
            print(tree.value)

        else:
            print("X_"+str(tree.feature_index), "<=", tree.threshold, "?", tree.info_gain)
            print("%sleft:" % (indent), end="")
            self.print_tree(tree.left, indent + indent)
            print("%sright:" % (indent), end="")
            self.print_tree(tree.right, indent + indent)

    def train_tree(self, dataset):
        ''' function to train the tree '''
        self.root = self.build_tree(dataset)

    def predict_single_sample(self, x, tree):
        #if reach the leaf --> the leaf node will have a value --> use it as prediction
        #recursively call to go down the branch of the decision tree to get the leaf node value
        if tree.value != None:
            return tree.value
        if x[tree.feature_index] <= tree.threshold:
            return self.predict_single_sample(x, tree.left)
        else:
            return self.predict_single_sample(x, tree.right)

    #function to return the prediction for all test samples in the testing dataset
    def predict(self, test_data):
        predictions = np.zeros(test_data.shape[0])
        for i in range(test_data.shape[0]):
            predictions[i] = self.predict_single_sample(test_data[i,:-1],self.root)
        return predictions

#function to calculate the prediction accuracy of the desicion tree classifier
def accuracy(ground_truth, predictions):
    return np.sum(ground_truth == predictions) / ground_truth.shape[0]
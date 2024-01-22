from graph import *
from path_io import *
from sol import Sol
import os
from DT import *

dirname = "datas"
LocFile = os.path.join(dirname, 'mock_locations.csv')
EdgeFile = os.path.join(dirname, 'mock_edges.csv')
# The speed info is in graph.py

#train the tree
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#initialize the decision tree with maximum depth 3
classifier = DecisionTree(max_depth=3)

def train_tree():
    data = pd.read_csv('raw_data.txt', encoding='utf-16-le', sep='\t')
    #print(data)
    #convert the data into numpy array
    raw_data = data.values
    #decode label as number 1 - 5
    #great --> 5; good --> 4; ok --> 3; low --> 2; very low --> 1
    num_samples, num_features = raw_data.shape
    utility = np.zeros(num_samples)
    index = 0
    for val in raw_data[:,0]:
        if val >= 0.8:
            utility[index] = 5
        elif val >= 0.6 and val < 0.8:
            utility[index] = 4
        elif val >= 0.4 and val < 0.6:
            utility[index] = 3
        elif val >= 0.2 and val < 0.4:
            utility[index] = 2
        else:
            utility[index] = 1
        index += 1
    #label the utility scores
    labelled_data = np.copy(raw_data)
    #move the labels to the last column of dataset
    labelled_data = np.delete(labelled_data, 0, axis=1)
    labelled_data = np.concatenate((labelled_data, utility.reshape(-1,1)), axis=1)

    train_data = labelled_data[200:1000,:]
    test_data = labelled_data[0:200,:]

    classifier.train_tree(train_data)
    #make prediction on the test data
    predictions = classifier.predict(test_data)
    acc = accuracy(test_data[:,-1],predictions)
    print(acc,"decision tree accuracy")
    Path.TREE = classifier

def RoundTripRoadTrip (startLoc:str, LocFile:str, EdgeFile:str, maxTime:float, resultFile:str, x_mph:float):
    Edge.SPEED=x_mph
    myGraph = Graph(startLoc, read_vertex(LocFile),read_edge(EdgeFile))
    sol=Sol(maxTime, myGraph, myGraph.start)
    with Output(resultFile,myGraph, maxTime, x_mph) as o:
        print("Do you want to continue? (yes/no)")
        while input()=="yes":
            # add prompt words for the user
            ans:Road=sol.search_once()
            if ans:
                o.write_road(ans,startLoc)
                print("Do you want to continue? (yes/no)")
            else:
                o.write_done(sol.elapsed)
                break
        o.write_done(sol.elapsed)

# 3 test runs
train_tree()
#RoundTripRoadTrip("NashvilleTN", LocFile, EdgeFile, 300, "test1.txt",60)
#RoundTripRoadTrip("CincinnatiOH", LocFile, EdgeFile, 300, "test2.txt",60)
RoundTripRoadTrip("DenverCO", LocFile, EdgeFile, 300, "test3.txt",60)
# Project description

This project implements a road trip recommender system on a road graph. Implement a decision tree from scratch that can predict the utility of a road. Implement a utility-driven search algorithm that can find round trips in the road graph with highest utility within the constraint of total travel time. The user can specify the starting location of the round trip and also give data input of the number of different kinds of themes(characteristics like history and culture, natural landscape, or city view) encountered in a road with its corresponding utility to the decision tree to train.

The decision tree calculates the utility of a road (a sequence of vertices and edges) given all the themes (characteristics) encountered (each vertex and edge may have a theme) on the road as the input. In our project, the theme for each vertex or edge is an integer value ranging from 0-9. The decision tree counts the total number of different themes on a road. Note that this doesn’t provide estimation of utilities of individual edge or vertex, it works on a road. 

The graph of all vertices and edges is stored as an adjacency matrix. There is no time stayed at both each vertex and edge, as the decision tree works only for roads, not individual edges and vertices. There is only traverse time of edges, which are determined by edge length and the travel speed. Each vertex and edge have an additional integer ranging from [0,9] to represent the theme of it.

The search algorithm is Anytime Iterative Deepening Heuristic DFS. 
Iterative Deepening: bounded by travel time, which is the time needed to traverse all the edges. 
Heuristic: the utility computed by the decision tree is used as heuristic, which is used to determine the order of paths put into the frontier (Heuristic DFS). 
DFS: tends to find longer valid paths. Also, note that repeated vertices are ignored.


We used Python 3.11 for this assignment.

See details for the decision tree in DT.py. The data used for training the decision tree is raw_data.txt

The generated data are mock_edges.csv and mock_locations.csv under the "datas" directory.

For solution, see sol.py for details.

For definition of graph, edge, vertex, and path, see graph.py for details.

We trained the decision tree in main.py.

See test results in test1.txt, test2.txt, test3.txt. 
Note: The utility score sometimes does not change because the road is cycling in a part of the graph. Thus, the themes encountered do not increase so the decision tree outputs the same utility score for these roads.

Reflection on the use of AI: we didn't use AI to help our programming for this assignment.

All our test cases had possible solutions. All solutions met the hard time constraints.



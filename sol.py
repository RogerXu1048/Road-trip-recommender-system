from typing import *
from graph import *
from time import time
from typing import Iterator, Tuple, List, Optional, Sized

"""
We're using a anytime heuristic dfs bounded by total travel time and utility as heuristic. The dfs will find a round trip 
ignoring repeated vertices like assignment 2, bounded by a maximum travel time, and rustically using the utility score. This means that the algorithm may return any path(potentially with repeated vertices) starting and ending 
at the given vertex that satisfy the time constraint, including circling around certain parts of the graph that 
have a very high utility.

The utility score has values 1,2,3,4,5. 

"""

class Sol:
    max_time: Final[float]
    G: Final[Graph]
    fr: Final[list[Path]] = []  # frontier, `list` can be used as stack
    rs: Final[
        list[Road]] = []  # all the solution roads. this can be used as a heap as `Road` are ordered by total_pref.

    # add more when necessary
    def __init__(self, max_time: float, g: Graph, start: Vertex):  # add more if needed
        self.max_time = max_time
        self.G = g
        self.goal: Final[Vertex] = start
        self.start: Final[Vertex] = start

        self.elapsed: float = 0

        # add the edges from the starting vertex to the frontier
        mylist = []
        #sp = Path(Edge("begin", None, start, 0), None, True)

        for edge in self.G[start]:
            path = Path(edge, None)
            mylist.append(path)

        mylist.sort()
        for path in mylist:
            r = Road(path)
            if (r.total_time <= self.max_time):
                self.fr.append(path)

    def search_once(self) -> Road:
        start_time = time()
        while self.fr:
            top: Path = self.fr.pop()

            if top.dest is self.goal and top.prev is not None:
                r = Road(top)
                self.rs.append(r)
                self.elapsed += time() - start_time
                return r

            mylist = []

            for edge in self.G[top.dest]:
                path = Path(edge, top)
                mylist.append(path)
            mylist.sort()  # sort for heuristic dfs, so that higher perference are on top.
            mylist.reverse()

            for path in mylist:
                r = Road(path)
                if (r.total_time <= self.max_time):# bounded by time
                    self.fr.append(path)

from dataclasses import dataclass, field
from typing import *
from DT import *
import numpy as np



@dataclass(frozen=True)
class Vertex:
    name: Final[str] = field(hash=True)
    lat: Final[float] = field(hash=False)
    long: Final[float] = field(hash=False)
    #The theme for each vertex is an integer value ranges from 0 - 9 (represent one of the 10 themes) 
    # because the decision tree takes the number of each theme encountered as the input.
    theme: Final[int] = field(hash=False)

# mono-directional edge
@dataclass(eq=False, )
class Edge:
    name: Final[str] = field()
    src: Final[Optional[Vertex]] = field()  # two ends of an edge; use index of list
    dest: Final[Vertex] = field()
    length: Final[float] = field()  # length of this edge
    theme: Final[int] = field()
    #also needs to consider charastersics/utility here
    SPEED: ClassVar[float] = 60
    @property
    def traverse_time(self) -> float:
        return self.length / Edge.SPEED


class Path(Edge):
    # this is used to keep track of the previous track so we can trace the entire road back to beginning.
    prev: Final[Optional["Path"]]
    TREE: ClassVar[DecisionTree]

    def __init__(self, e: Edge, prev: Optional["Path"]):
        self.prev = prev
        super().__init__(e.name, e.src, e.dest, e.length, e.theme)

    # yields an iterator from the current node to the beginning.
    def trace_back(self)->Generator["Path",None,None]:
        cur=self
        while cur is not None:
            yield cur
            cur=cur.prev
    # utility is calculated using a decision tree from assignment 3.
    # that decision tree considers the characteristics of a complete road.
    def cal_utility(self)->float:
        count = [0] * 10
        for p in self.trace_back():
            count[p.dest.theme] += 1
            count[p.theme] += 1
        data = np.array(count)
        utility = Path.TREE.predict_single_sample(data,Path.TREE.root)
        return utility


    # sort using utility when put into stack.
    def __lt__(self, other: "Path") -> bool:
        return self.cal_utility() < other.cal_utility()


class Road(List[Path]):
    #example: `r = Road(p)
    def __init__(self, last: Path):
        super().__init__(last.trace_back())
        self.reverse()# need this because path traces from the last node to the first


    # returns the sum of all location and all edge utilities in a road trip
    @property
    def total_utility(self) -> float:
        return self[-1].cal_utility()# use the last path as this will include everything before it.

    # use this to get the time to compare with the bound for iterative deepening DFS.
    # computes the time required by a road trip in terms of its constituent edges and locations
    @property
    def total_time(self) -> float:
        return sum(map(Path.traverse_time.fget,self),0)

    # sort using total_utility when putting into all solutions.
    def __lt__(self, other: "Road") -> bool:
        return self.total_utility < other.total_utility


class Graph(Dict[Vertex,list[Edge]]):
    # store using adjency matrix similar to last time
    # this time directly use Vertex and edge
    start:Final[Vertex]

    def __init__(self, start_name: str, vs: Iterator[tuple[str, float, float]],
                 es: Iterator[tuple[str, str, str, float]]):
        super().__init__()
        names: dict[str, Vertex] = {}
        for name, lat, long,theme in vs:
            v: Vertex = Vertex(name, lat, long,theme)
            names[v.name] = v
            self[v] = []
        for name, a, b, l,theme in es:
            # forward
            v_a, v_b = names[a], names[b]

            e: Edge = Edge(name, v_a, v_b, l,theme)
            self[v_a].append(e)
            # reverse
            e: Edge = Edge(name, v_b, v_a, l,theme)
            self[v_b].append(e)
        self.start=names[start_name]

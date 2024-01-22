from typing import *
from graph import *
import csv, sys


def read_vertex(file_name: str) -> Iterator[tuple[str, float, float,int]]:
    with open(file_name, "r") as f:
        r = csv.reader(f)
        for row in r:
            if(len(row)>0):
                yield row[0], float(row[1]), float(row[2]), int(row[3])


def read_edge(file_name: str) -> Iterator[tuple[str, str, str, float,int]]:
    with open(file_name, "r") as f:
        r = csv.reader(f)
        for row in r:
            if(len(row)>0):
                yield row[0], row[1], row[2], float(row[3]),int(row[4])


class Output:
    file: Final[TextIO]
    g: Final[Graph]
    road_count: int = 0

    def __init__(self, output_file_name: str, graph: Graph, maxTime: float, mph: float):
        self.file = open(output_file_name, mode="w")
        self.g = graph
        self.max_time = maxTime
        self.x_mph = mph

    def write_road(self, r: Road, startName: str):
        self._write_road(r, startName, sys.stdout)
        self._write_road(r, startName, self.file)
        self.road_count += 1

    def _write_road(self, r: Road, startName: str, strm):
        print("solution %d %s %f %f" % (self.road_count, startName, self.max_time, self.x_mph), file=strm)
        distance = 0
        i = 0
        for path in r:
            e: Edge = path
            src: Vertex = path.src
            dest: Vertex = path.dest
            print("%d. %s %s %s %f " % (
            i + 1, src.name, dest.name, e.name, e.traverse_time),
                  file=strm)
            distance += e.length
            i += 1
        print("%s %f %f %f" % (startName, r.total_utility, distance, r.total_time), file=strm)

    def write_done(self, time: float):
        self._write_done(time, sys.stdout)
        self._write_done(time, self.file)

    def _write_done(self, time: float, strm):
        print("time: %f" % time, file=strm)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()

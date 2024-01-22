import csv,random
"""
Data are generated using the data from assignment 2, each vertex and edge are added a theme, which is a random integer in the range [0,9].
`Road Network ... .csv` are the original data from assignment 2 with the title row deleted. `mock ... .csv` are the data with generated theme variable. These, too, have no title row.
"""
def gen_vertexes(p:str,o:str):
    w=csv.writer(open(o,"w"),delimiter=",")
    with open(p,"r") as f:
        for r in csv.reader(f):
            w.writerow((r[0], float(r[1]), float(r[2]),random.randint(0,9)),)
def gen_edges(p:str,o:str):
    w=csv.writer(open(o,"w"),delimiter=",")
    with open(p,"r") as f:
        for r in csv.reader(f):
            w.writerow((r[0], r[1], r[2], float(r[3]),random.randint(0,9)),)

if __name__=="__main__":
    gen_vertexes("Road Network - Locations.csv","mock locations.csv")
    gen_edges("Road Network - Edges.csv","mock edges")
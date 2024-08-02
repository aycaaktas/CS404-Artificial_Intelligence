from pysat.formula import CNF
from pysat.solvers import Solver

def create_vertex_coloring_cnf(n, edges, k):
    cnf = CNF()
    
    # Each vertex must be colored
    for v in range(1, n+1):
        cnf.append([v + n * c for c in range(k)])
    
    # No vertex can have more than one color
    for v in range(1, n+1):
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-(v + n * c1), -(v + n * c2)])
    
    # No two adjacent vertices can have the same color
    for (v1, v2) in edges:
        for c in range(k):
            cnf.append([-(v1 + n * c), -(v2 + n * c)])
    
    return cnf

def k_colorable(n, edges, k):
    cnf = create_vertex_coloring_cnf(n, edges, k)
    solver = Solver()
    solver.append_formula(cnf)
    result = solver.solve()
    model = None
    if result:
        model = solver.get_model()
    solver.delete()
    return result, model

def interpret_model(model, n, k):
    coloring = {}
    for var in model:
        if var > 0:
            vertex = ((var - 1) % n) + 1
            color = (var - 1) // n
            coloring[vertex] = color + 1

    sorted_coloring = {vertex: coloring[vertex] for vertex in sorted(coloring)}
    return sorted_coloring

def find_chromatic_number(n, edges):
    k = 1
    while True:
        is_colorable, model = k_colorable(n, edges, k)

        if is_colorable:
            coloring = interpret_model(model, n, k)
            print(f"The graph is colorable with {k} colors. Coloring: {coloring}")
            return k, coloring  
        else:
            print(f"The graph is not colorable with {k} colors.")
            k += 1


def read_graph_from_file(filename):
    with open(filename, 'r') as file:
        edges = []
        n = m = 0
        for line in file:
            if line.startswith('c'):
                continue  # Skip comment lines
            elif line.startswith('p'):
                parts = line.split()
                n = int(parts[2])
                m = int(parts[3])
            elif line.startswith('e'):
                parts = line.split()
                edges.append((int(parts[1]), int(parts[2])))
        return n, edges

def main():

    filename = 'example1.col'  # Path to the graph file
    n, edges = read_graph_from_file(filename)

    print("-"*50)

    k=3
    result,model=k_colorable(n, edges, k)
    
    if result:
        solution = interpret_model(model, n, k)
        print(f"The graph is colorable with {k} colors. Coloring: {solution}")
    else:
        print(f"The graph is not colorable with {k} colors.")

    print("-"*50)

    chromatic_number, last_coloring = find_chromatic_number(n, edges)
    print(f"The chromatic number of the graph is {chromatic_number}.")
    print(f"Valid coloring with chromatic number: {last_coloring}")

    print("-"*50)

if __name__ == '__main__':
    main()
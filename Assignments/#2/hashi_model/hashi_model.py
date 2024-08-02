import numpy as np
from inter import inter
from easy import easy
from hard import hard

n = 7

def generate_output(grid, bridges, islands):
    output = [['.' for _ in range(n)] for _ in range(n)]  

    def bridge_char(number_of_bridges, horizontal):
        if number_of_bridges == 1:
            return '-' if horizontal else '|'
        elif number_of_bridges == 2:
            return '=' if horizontal else 'x'
    
    for (row, col, _) in islands:
        output[row-1][col-1] = str(grid[row-1][col-1])

    for i, (row1, col1, _) in enumerate(islands):
        for j, (row2, col2, _) in enumerate(islands):
            if i != j and bridges[i][j] > 0:
                bridge = bridges[i][j]
                if row1 == row2:  # Horizontal bridge
                    for col in range(min(col1, col2) + 1, max(col1, col2)):
                        output[row1-1][col-1] = bridge_char(bridge, True)
                elif col1 == col2:  # Vertical bridge
                    for row in range(min(row1, row2) + 1, max(row1, row2)):
                        output[row-1][col1-1] = bridge_char(bridge, False)
    
    return '\n'.join(''.join(row) for row in output)

def is_connected(adj_matrix):

    num_nodes = len(adj_matrix)
    visited = [False] * num_nodes

    def dfs(node):
        visited[node] = True
        for neighbor, connected in enumerate(adj_matrix[node]):
            if connected and not visited[neighbor]:
                dfs(neighbor)

    dfs(0)

    return all(visited)

easy_islands = easy["islands"]
easy_input = np.array(easy["input"]).reshape((n, n))
easy_bridges = np.array(easy["bridges"]).reshape((len(easy_islands), len(easy_islands)))

print("Easy solution:")
print(generate_output(easy_input, easy_bridges, easy_islands))
print("Is connected?:", is_connected(easy_bridges))

inter_islands = inter["islands"]
inter_input = np.array(inter["input"]).reshape((n, n))
inter_bridges = np.array(inter["bridges"]).reshape((len(inter_islands), len(inter_islands)))

print("Inter solution:")
print(generate_output(inter_input, inter_bridges, inter_islands))
print("Is connected?:", is_connected(inter_bridges))

hard_islands = hard["islands"]
hard_input = np.array(hard["input"]).reshape((n, n))
hard_bridges = np.array(hard["bridges"]).reshape((len(hard_islands), len(hard_islands)))

print("Hard solution:")
print(generate_output(hard_input, hard_bridges, hard_islands))
print("Is connected?:", is_connected(hard_bridges))


from queue import PriorityQueue
from classes import Node, GameBoard, Move
import json
import copy


def print_matrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))

def solution(initial_node, goal_node) :
    
    print("---------------------")
    print_matrix(initial_node.state.grid)
    solution2(goal_node)
    


def solution2(goal_node) :
   
    if goal_node.parent is None:
        return
    solution2(goal_node.parent)
    print("---------------------")
    print("Action Direction:",goal_node.direction)
    print_matrix(goal_node.state.grid)
    print("---------------------")
   


def SUCC_H(node) :
    
    children = list()

    for movement in Move:

        child_state = copy.deepcopy(node.state)
        child_node = Node(child_state,0, node,movement)
        child_node.state.move_cell(movement)
        child_node.state.g += node.state.g
        child_node.f = child_node.state.g + child_node.state.heuristic_calc(movement) 
        
        children.append(child_node)

    return children

def SUCC_H2(node) :
    
    children = list()

    for movement in Move:

        child_state = copy.deepcopy(node.state)
        child_node = Node(child_state,0, node,movement)
        child_node.state.move_cell(movement)
        child_node.state.g += node.state.g
        child_node.f = child_node.state.g + child_node.state.heuristic_calc2(movement) 
        
        children.append(child_node)

    return children

def a_star_search(grid) :

    closed = list()
    frontier = PriorityQueue()
    states_in_frontier = set()
    states_in_closed = set()  

    start_state = GameBoard(grid)
    initial_node = Node(start_state,0, None,None)
    frontier.put(initial_node)

    while not frontier.empty():
        n = frontier.get()
        states_in_frontier.add(n.state)

        if n.state.goal_test():
            solution(initial_node, n)
            print("distance traveled:", n.state.g)
            print("number of expanded nodes:", len(closed))
            return
        
        children=SUCC_H(n)
        for s in children:

            if s.state not in states_in_frontier and s.state not in states_in_closed:
                frontier.put(s)

            temp = list()
            while (not frontier.empty()):
                popped = frontier.get()
                if (s.state.grid == popped.state.grid and s.f < popped.f):
                    popped.f = s.f
                    popped.state.g=s.state.g
                    popped.parent = n
                temp.append(popped)

            for elem in temp:
              frontier.put(elem)

        closed.append(n)
        states_in_closed.add(n.state)



def a_star_search2(grid) :

    closed = list()
    frontier = PriorityQueue()
    states_in_frontier = set()
    states_in_closed = set()  

    start_state = GameBoard(grid)
    initial_node = Node(start_state,0, None,None)
    frontier.put(initial_node)

    while not frontier.empty():
        n = frontier.get()
        states_in_frontier.add(n.state)

        if n.state.goal_test():
            solution(initial_node, n)
            print("distance traveled:", n.state.g)
            print("number of expanded nodes:", len(closed))
            return
        
        children=SUCC_H2(n)
        for s in children:

            if s.state not in states_in_frontier and s.state not in states_in_closed:
                frontier.put(s)

            temp = list()
            while (not frontier.empty()):
                popped = frontier.get()
                if (s.state.grid == popped.state.grid and s.f < popped.f):
                    popped.f = s.f
                    popped.state.g=s.state.g
                    popped.parent = n
                temp.append(popped)

            for elem in temp:
              frontier.put(elem)

        closed.append(n)
        states_in_closed.add(n.state)







def read_matrices(file_path):
   with open(file_path, 'r') as file:
        data = file.read()
        grids = json.loads(data)
        return grids

def process_matrices(file_path, level):
    print("--------------------------------------------------------------------------------------------------------")
    print("The difficulty level is:",level)
    matrices = read_matrices(file_path)
    a_star_search(matrices[0]) 

    


def main():

    process_matrices('easy_grids.txt', 'easy')
    process_matrices('intermediate_grids.txt', 'intermediate')
    process_matrices('difficult_grids.txt', 'difficult')

if __name__ == "__main__":
    main()

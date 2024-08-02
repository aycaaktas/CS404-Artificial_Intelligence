

from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt

# Initialize the graph
G = nx.DiGraph()

def save_graph(file_path):
    # Define node positions using a layered layout to enhance readability
    pos = nx.multipartite_layout(G, subset_key="layer")
    labels = nx.get_node_attributes(G, 'label')
    
    # Color scheme for different types of nodes
    color_map = []
    for node in G:
        if 'Max' in G.nodes[node]['label']:
            color_map.append('lightgreen')
        elif 'Min' in G.nodes[node]['label']:
            color_map.append('lightblue')
        elif 'Pruned' in G.nodes[node]['label']:
            color_map.append('lightgray')
        else:
            color_map.append('salmon')

    plt.figure(figsize=(20, 15))  # Larger figure size
    nx.draw(G, pos, with_labels=True, labels=labels, node_color=color_map, node_size=7000, font_size=9, arrowstyle='-|>', arrowsize=12)
    plt.savefig(file_path)
    plt.close()

#Minimax function for alpha beta pruning
def minimax(state, isMax, alpha, beta, depth=0, node_id="Root", layer=0):
        
    #AI is max
        
    currentState = HashiGame(state["board_config"])
    currentState.modifier(state["islands"], state["bridges"], state["scores"], state["turn"])

    # If terminal return score of the AI
    if currentState.is_terminal():
        node_label = f"Terminal\nScore={currentState.scores['ai']}"
        G.add_node(f"{node_id} Terminal", label=node_label, layer=layer)
        G.add_edge(node_id, f"{node_id} Terminal")
        return (currentState.scores["ai"], "")
        
    if isMax: #Max Node

        node_type = "Max" 
        node_label = f"{node_type}\nA={alpha}, B={beta}"
        G.add_node(node_id, label=node_label, layer=layer) 
         
        bestVal = -1000
        bestMove = None
        legal_moves = currentState.legal_moves()
        
        #While exploring the possible moves, prune the unnecessary moves
        for move in legal_moves:
             
            child_id = f"{node_id} {move}"
            move_label = f"Move: {move}\nDepth={depth+1}"
            G.add_node(child_id, label=move_label, layer=layer+1)
            G.add_edge(node_id, child_id)
            
            #Calculating the game board after the possible move 
            childState = HashiGame(state["board_config"])
            childState.modifier(state["islands"], state["bridges"], state["scores"], state["turn"])
            childState.auto_play(move) # state transition function 
            childStateDict = {"board_config": childState.board, "islands": childState.islands, "bridges": childState.bridges, "scores": childState.scores, "turn": "human"}
                
            #Max Eval
            value_temp = minimax(childStateDict, False, alpha, beta, depth + 1, child_id, layer + 1)
            value = value_temp[0]
            bestVal = max(bestVal, value)
            if bestVal == value:
                bestMove = move
            alpha = max(alpha, bestVal)
            
            #Prunning
            if beta <= alpha:
                prune_label = "Pruned"
                G.add_node(f"{child_id} Prune", label=prune_label, layer=layer+2)
                G.add_edge(child_id, f"{child_id} Prune")
                break
        #Return best move
        G.nodes[node_id]['label'] += f"\nBest={bestVal}"
        return (bestVal, bestMove)
        
    else: #Min Node

        node_type = "Min"    
        node_label = f"{node_type}\nA={alpha}, B={beta}"
        G.add_node(node_id, label=node_label, layer=layer)

        bestVal = 1000
        bestMove = None
        legal_moves = currentState.legal_moves()

        #While exploring the possible moves, prune the unnecessary moves
        for move in legal_moves:

            child_id = f"{node_id} {move}"
            move_label = f"Move: {move}\nDepth={depth+1}"
            G.add_node(child_id, label=move_label, layer=layer+1)
            G.add_edge(node_id, child_id)
            
            #Calculating the game board after the possible move 
            childState = HashiGame(state["board_config"])
            childState.modifier(state["islands"], state["bridges"], state["scores"], state["turn"])
            childState.auto_play(move) # state transition function
            childStateDict = {"board_config": childState.board, "islands": childState.islands, "bridges": childState.bridges, "scores": childState.scores, "turn": "ai"}

            #Min Eval
            value_temp = minimax(childStateDict, True, alpha, beta, depth + 1, child_id, layer + 1)
            value = value_temp[0]
            bestVal = min(bestVal, value)
            if bestVal == value:
                bestMove = move
            beta = min(beta, bestVal)

            #Prunning
            if beta <= alpha:
                prune_label = "Pruned"
                G.add_node(f"{child_id} Prune", label=prune_label, layer=layer+2)
                G.add_edge(child_id, f"{child_id} Prune")
                break
        #Return best move
        G.nodes[node_id]['label'] += f"\nBest={bestVal}"        
        return (bestVal, bestMove)

class HashiGame:
    def __init__(self, board_config, player_turn="human"):# default game turn is at human
        self.size = len(board_config)
        self.board = deepcopy(board_config) 
        self.islands = [] # keeps a tuple island information as: ( row, colomn , label, current )
        self.bridges = {} # key is the coordinates of the two islands and the value is the number of bridges between them
        self.scores = {"human": 0, "ai": 0}  
        self.player_turn = deepcopy(player_turn)  
        self.init_islands()
    
    #modifies the game instance with given state attributes
    def modifier(self, islands, bridges, scores, turn):
        self.islands = deepcopy(islands)  
        self.bridges = deepcopy(bridges)
        self.scores = deepcopy(scores)
        self.player_turn = deepcopy(turn) 


    def init_islands(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j].isdigit():
                    label = int(self.board[i][j])
                    self.islands.append((i, j, label, 0))

    def print_board(self):
        for row in self.board:
            print(' '.join(row))
        print(f"Scores -> Player Human: {self.scores['human']}, Player AI: {self.scores['ai']}")
        print()

    # Game ends when there is no possible moves left 
    def is_terminal(self):
        return True if len(self.legal_moves()) == 0 else False

    # Checks the bridges dictinary to check whether a new bridge can be put between them : There can be at most 2 bridges between two islands   
    def can_add_bridge(self, i1, j1, i2, j2, direction):
        
        key = tuple(sorted([(i1, j1), (i2, j2)]))
        if key in self.bridges:
            return self.bridges[key] < 2  
        return True
    
    #Calculates all possible moves that can be played by the current player and stores them in an array. 
    def legal_moves(self):
        moves = []
        for idx, (i1, j1, label1, current1) in enumerate(self.islands):
            if label1 == 0:
                #There are two possible moves, one of them is labelling the empty islands with either 3 or 4 
                moves.append(('label', i1, j1, 3))
                moves.append(('label', i1, j1, 4))
                continue
            if current1 < label1:
                #There are two possible moves, the other one is placing a bridge between two labelled island.
                for idy, (i2, j2, label2, current2) in enumerate(self.islands):
                    if idx != idy and current2 < label2:
                        if label2 == 0:  
                           continue
                        if i1 == i2:  #horizontal bridge
                            range_min, range_max = sorted([j1, j2])
                            if all(self.board[i1][k] == '.' for k in range(range_min + 1, range_max)) or all(self.board[i1][k] == '-' for k in range(range_min + 1, range_max)):
                                if self.can_add_bridge(i1, j1, i2, j2, 'h'):
                                    moves.append(('h', i1, j1, i2, j2))
                        elif j1 == j2:  # vertical bridge
                            range_min, range_max = sorted([i1, i2])
                            if all(self.board[k][j1] == '.' for k in range(range_min + 1, range_max)) or all(self.board[k][j1] == '|' for k in range(range_min + 1, range_max)):
                                if self.can_add_bridge(i1, j1, i2, j2, 'v'):
                                    moves.append(('v', i1, j1, i2, j2))
        return moves
 
    # State transition function for placing a bridge. Modifies the game board and calculates the both player's score
    def apply_move(self, move):

        direction, i1, j1, i2, j2 = move
        key = tuple(sorted([(i1, j1), (i2, j2)]))
        if key in self.bridges:
             bridge_count = self.bridges[key] + 1
        else:
            bridge_count = 1  
        self.bridges[key] = bridge_count

        if direction == 'h':
            symbol = '=' if bridge_count == 2 else '-'
            for k in range(min(j1, j2) + 1, max(j1, j2)):
                self.board[i1][k] = symbol
        elif direction == 'v':
            symbol = 'x' if bridge_count == 2 else '|'
            for k in range(min(i1, i2) + 1, max(i1, i2)):
                self.board[k][j1] = symbol

        for index, (i, j, label, current) in enumerate(self.islands):
            if (i, j) == (i1, j1) or (i, j) == (i2, j2):
                self.islands[index] = (i, j, label, current + 1)
                if current + 1 == label:
                    self.scores[self.player_turn] += label
                    opponent = "ai" if self.player_turn == "human" else "human"
                    self.scores[opponent] -= label
                    

    # Takes input from the human checks the validity of the move
    def human_move(self):
        valid = False
        while not valid:
            move_input = input("Enter your move (format for bridge: 'h/v row1 col1 row2 col2' or label: 'label row col num'): ")
            print("The input is:",move_input)
            try:
                parts = move_input.split()
                #placing a bridge
                if parts[0] in ['h', 'v']:  
                    direction, i1, j1, i2, j2 = parts
                    i1, j1, i2, j2 = int(i1), int(j1), int(i2), int(j2)
                    move = (direction, i1, j1, i2, j2)
                    if move in self.legal_moves():
                        self.apply_move(move)
                        valid = True
                    else:
                        print("Invalid bridge move, please try again.")
                #Labeling an empty island
                elif parts[0] == 'label':  
                    _, row, col, num = parts
                    row, col, num = int(row), int(col), int(num)
                    if self.board[row][col] == '0' and num in [3, 4]:  
                        self.board[row][col] = str(num)
                        for index, (i, j, label, current) in enumerate(self.islands):
                            if i == row and j == col:
                                self.islands[index] = (row, col, num, current)  
                                break
                        valid = True
                    else:
                        print("Invalid label move, please ensure you are labeling an empty island and the label must be '3' or '4'.")
                else:
                    print("Unknown command, please enter a valid move.")
            except Exception as e:
                print(f"Error parsing input: {e}. Please try again.")
                

                
                
    #Finds the best move for the AI at the current state (game board)          
    def ai_move(self,move_no):
        
        
        currentState = {"board_config": self.board, "islands": self.islands, "bridges": self.bridges, "scores": self.scores, "turn": self.player_turn}
        print("Minimax is working", "-"*50)
        best_temp = minimax(currentState, True, -1000, 1000)
        save_graph(f"minimax_tree_{move_no}.png")
        print("Minimax is done", "-"*50)
        return best_temp[1]

    #The main game play function. It will countinue until a terminal state is reached.
    def play_game(self):
        move_count=0
        print("-"*50)
        print("The initial state of the game board:")
        self.print_board()
        print("-"*50)
        while not self.is_terminal():
            move_count +=1
            print("The current Move is:",move_count)
            if self.player_turn == "human":
                print("-"*50)
                print("Human's turn:")
                print(self.legal_moves())
                self.human_move()
                print("The state of the game board after the move:")
                self.print_board()
                self.player_turn="ai"
                print("-"*50)

            elif self.player_turn == "ai":
                print("-"*50)
                print("AI's turn:")
                print(self.legal_moves())
                best_move = self.ai_move(move_count)
                self.auto_play(best_move)
                print("The state of the game board after the move:")
                self.print_board()
                self.player_turn="human"
                print("-"*50)

    #State transition function for the AI player.           
    def auto_play(self, move_input):
        
        #Assumes legal move 
        
        parts = move_input
        
        if parts[0] in ['h', 'v']:  
            direction, i1, j1, i2, j2 = parts
            i1, j1, i2, j2 = int(i1), int(j1), int(i2), int(j2)
            move = (direction, i1, j1, i2, j2)
            self.apply_move(move)
            
        elif parts[0] == 'label':  
            _, row, col, num = parts
            row, col, num = int(row), int(col), int(num)
            if self.board[row][col] == '0' and num in [3, 4]:  
                self.board[row][col] = str(num)
                for index, (i, j, label, current) in enumerate(self.islands):
                    if i == row and j == col:
                        self.islands[index] = (row, col, num, current)  
                        break
                    
#Instance number one AI RUN
initial_config = [
    ["1", ".", "1", "."],
    [".", "0", ".", "."],
    [".", ".", ".", "."],
    [".", "2", ".", "0"]
]

#Instance number two HUMAN RUN
initial_config_2 = [
    ["2", ".", "2", "."],
    [".", ".", ".", "."],
    ["1", ".", "0", "."],
    [".", "2", ".", "0"]
]


game = HashiGame(deepcopy(initial_config_2))
game.play_game()





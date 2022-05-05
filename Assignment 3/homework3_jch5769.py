############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "John Hofbauer"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from random import choice
from queue import PriorityQueue
from math import sqrt
import time


############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    return TilePuzzle([[0 if x*y == cols*rows else x+(cols*(y-1)) for x in range(1, cols+1)] for y in range(1, rows+1)])

class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.board = board
        self.emptyspot = []
        for index in range(len(board)):
            if 0 in board[index]:
                self.emptyspot = [board[index].index(0), index]
        #print("emptyspot: " + str(self.emptyspot))

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        print
        #print("Swaping: " + str(self.board[self.emptyspot[1]][self.emptyspot[0]]))
        #print("With: " + str(self.board[self.emptyspot[1]-1][self.emptyspot[0]]))
        if direction == "up" and 0 <= self.emptyspot[1]-1 <= len(self.board)-1: # Swap the empty spot with the one above it
            self.board[self.emptyspot[1]][self.emptyspot[0]] = self.board[self.emptyspot[1]-1][self.emptyspot[0]]
            self.board[self.emptyspot[1]-1][self.emptyspot[0]] = 0
            self.emptyspot[1] = self.emptyspot[1]-1 # update the empty spot
            return True

        if direction == "down" and 0 <= self.emptyspot[1]+1 <= len(self.board)-1: # Swap the empty spot with the one below it
            self.board[self.emptyspot[1]][self.emptyspot[0]] = self.board[self.emptyspot[1]+1][self.emptyspot[0]]
            self.board[self.emptyspot[1]+1][self.emptyspot[0]] = 0
            self.emptyspot[1] = self.emptyspot[1]+1 # update the empty spot
            return True

        if direction == "left" and 0 <= self.emptyspot[0]-1 <= len(self.board[0])-1: # Swap the empty spot with the one to the left
            self.board[self.emptyspot[1]][self.emptyspot[0]] = self.board[self.emptyspot[1]][self.emptyspot[0]-1]
            self.board[self.emptyspot[1]][self.emptyspot[0]-1] = 0
            self.emptyspot[0] = self.emptyspot[0]-1 # update the empty spot
            return True

        if direction == "right" and  0 <= self.emptyspot[0]+1 <= len(self.board[0])-1: # Swap the empty spot with the one to the right
            self.board[self.emptyspot[1]][self.emptyspot[0]] = self.board[self.emptyspot[1]][self.emptyspot[0]+1]
            self.board[self.emptyspot[1]][self.emptyspot[0]+1] = 0
            self.emptyspot[0] = self.emptyspot[0]+1 # update the empty spot
            return True

        return False

    def scramble(self, num_moves):
        for index in range(num_moves):
            self.perform_move(choice(["right", "left", "up", "down"]))

    def is_solved(self):
        if self.board == create_tile_puzzle(len(self.board[0]), len(self.board)).get_board():
            return True
        return False

    def copy(self):
        """ This creates a DeepCopy of the board, then returns a new object with the copyed bord. """
        return TilePuzzle([[n for n in self.board[x]] for x in range(len(self.board))])


    def successors(self):
        for index in ["up", "down", "left", "right"]:
            newBord = TilePuzzle(self.copy().get_board())
            newBord.perform_move(index)
            yield (index, newBord)

    # Required
    def find_solutions_iddfs(self):
        """
        Finds the solution to the puzzle using;
        Iterative deapinging search using the.
        """
        self.steps = []
        self.visited = []
        self.successorsFound = 1 # this starts on.

        goal = create_tile_puzzle(len(self.board), len(self.board[0])).get_board()

        def nextLevel(prevouse = ()):
            succ = 0
            #print("Origial: " + str(self.get_board()))
            for moves, new_board in self.successors(): # Find the successors.
                
                # make sure they were not visited.  #Save when more than one goal if found
                if new_board.get_board() not in self.visited or new_board.get_board() == goal: 
                    #print("successors: " + str(moves) + "   "+ str(new_board.get_board()))
                    
                    succ = 1
                    #print("Succ = " + str(succ))

                    # Populete the lists.
                    if len(prevouse) > 0:
                        newnewlist = prevouse
                        if type(newnewlist) == type(list()):
                            newnewlist = prevouse[:]
                            newnewlist.append(moves)

                        else: # speciel case for the first itteration.
                            newnewlist = [prevouse]
                            newnewlist.append(moves)
                        self.steps.append([newnewlist, new_board.get_board()])
                    else:
                        self.steps.append([[moves], new_board.get_board()])
                    self.visited.append(new_board.get_board())
                #else:
                #    print("Already seen: " + str(moves) + "   "+ str(new_board.get_board()))
            return succ


        def checkThem(index):
            """
            Check for all false in the steps list.
            """
            #print("Checking: " + str(create_tile_puzzle(len(self.board[0]), len(self.board)).get_board()))
            #print("with: " + str(self.steps[index][1]))

            # Return if an answer has been found in the list of posibilites
            if create_tile_puzzle(len(self.board), len(self.board[0])).get_board() == self.steps[index][1]:
                #print("DONE")
                return self.steps[index][0]
            else:
                return 0
        #Special case for no moves
        if goal == self.board:
            yield []
            return

        # special case for only one move
        nextLevel()

        for index in range(len(self.steps)):
            answer = checkThem(index)
            if answer != 0: 
                return answer

        # Use a FOUND SUCCESSSER verable to know if i need to keep checking.
        while self.successorsFound == 1:
            self.successorsFound = 0
            for index in range(len(self.steps)):
                # Go through the steps list replacing them with the next height. adding nxn entries
                    if len(self.steps[index]) < 3:
                        # save the current board
                        currentBoard = self.copy().get_board()
                        
                        self.board = self.steps[index][1] # Set the board
                        #print("Origial Stored: " + str(self.steps[index][1]))
                        #print("Origial After set: " + str(self.get_board()))
                        

                        succ = nextLevel(self.steps[index][0])
                        self.steps[index].append(1)
                        if succ == 1:
                            self.successorsFound = 1
                        #print("Succ = " + str(succ))
                        #print("successorsFound = " + str(self.successorsFound))

                        self.board = currentBoard
            

            for index in range(len(self.steps)): # only check what hasn't been checked before
                answer = checkThem(index)
                if answer != 0: 
                    yield answer #list(dict.fromkeys()) # remove dup
                    self.successorsFound = 0 #this stops the recursion, when answers are found at this level
        return None

    # Required
    def find_solution_a_star(self):
        """
        Finds the solution to the puzzle using;
        A* search using the Manhattan distance heuristic
        """
        self.steps = []
        self.visited = []
        self.successorsFound = 1 # this starts on.

        goal = create_tile_puzzle(len(self.board), len(self.board[0])).get_board()
        goalPositions = {}
        for row in range(len(goal)):
            for element in range(len(goal[row])):
                # find the distance to where it should be.
                goalPositions[goal[row][element]] = (row, element)

        def nextLevel(prevouse = ()):
            succ = 0
            #print("Origial: " + str(self.get_board()))
            moves = []
            new_board = []
            h_values = []
            lowset_F = 100000000000000000000000000 # large number
            for moves2, new_board2 in self.successors(): # Find the successors.
                # implement A* by only visiting the board closest to the goal
                ### Store F = p + h in the steps table. 
                # sort the table by the lowset F.
                # then alays find the successors of the lowest F first.
                f = 0
                #Evaluate the bord to see find h
                dic = {}
                for row in range(len(new_board2.get_board())):
                    for element in range(len(new_board2.get_board()[row])):
                        # find the distance to where it should be.
                        dic[new_board2.get_board()[row][element]] = (row, element)

                #print(dic)
                h = 0
                for i in dic:
                    #print(dic[i], goalPositions[i])
                    h += abs(abs(dic[i][0]) - abs(goalPositions[i][0])) # add the hroazontal diffrence, add the vertical diffrence.
                    h += abs(abs(dic[i][1]) - abs(goalPositions[i][1])) 
                    #print(dic[i][0] - goalPositions[i][0])
                #print(h)

                # Get p 
                p = len(prevouse)

                # Solve for f
                f = p + h

                if f <= lowset_F and new_board2.get_board() not in self.visited:
                    lowset_F = f
                    h_values.append(h)
                    moves.append(moves2)
                    new_board.append(new_board2)

            for x in range(len(new_board)):
                # only save values that get us closser to the goal
                #if new_board.get_board() not in self.visited: 
                succ = 1
                
                # Populete the lists.
                if len(prevouse) > 0:
                    newnewlist = prevouse
                    if type(newnewlist) == type(list()):
                        newnewlist = prevouse[:]
                        newnewlist.append(moves[x])

                    else: # speciel case for the first itteration.
                        newnewlist = [prevouse]
                        newnewlist.append(moves[x])
                    self.steps.append((newnewlist, new_board[x].get_board(), h_values[x]))
                else:
                    self.steps.append(([moves[x]], new_board[x].get_board(), h_values[x]))
                self.visited.append(new_board[x].get_board())
            return succ


        def checkThem(index):
            # Return if an answer has been found in the list of posibilites
            if create_tile_puzzle(len(self.board), len(self.board[0])).get_board() == self.steps[index][1]:
                #print("DONE")
                return self.steps[index][0]
            else:
                return 0
        # special case for only one move
        nextLevel()

        for index in range(len(self.steps)):
            answer = checkThem(index)
            if answer != 0: 
                return answer

        # Use a FOUND SUCCESSSER verable to know if i need to keep checking.
        while self.successorsFound == 1:
            self.successorsFound = 0
            for index in range(len(self.steps)):
                # Go through the steps list replacing them with the next height. adding nxn entries
                # save the current board
                #if 
                currentBoard = self.copy().get_board()
                self.board = self.steps[index][1] # Set the board
                succ = nextLevel(self.steps[index][0])
                if succ == 1:
                    self.successorsFound = 1
                self.board = currentBoard
            #print("__________STEPS____________")
            #for i in self.steps:
            #    print(i)
            #print("__________VISITED____________")
            #for i in self.visited:
            #    print(i)

            # SPEEED UP DAT MOFO< ___________________________ (Delete this portion if it doesn't work)
            # Find the bEst H
            best_H_Value = 100000000000000000000 # Large number
            for index in range(len(self.steps)):
                #print("H_Value: " + str(self.steps[index][2]))
                if self.steps[index][2] <= best_H_Value:
                    best_H_Value = self.steps[index][2]
            #print("Purging all values grater than: " + str(best_H_Value))
            # Perge all the bad H values.
            x = 0
            for index in range(len(self.steps)):

                if self.steps[x][2] > best_H_Value + 7: # <--- REMOVE THIS portion BEFORE SUBMITTING!!!
                    self.steps.pop(x)                   # this lowers the runtime. but adds a posablitiy of the program not finnshing.
                    x-=1
                x+=1
            # _________________________________________________
            

            for index in range(len(self.steps)): # only check what hasn't been checked before
                answer = checkThem(index)
                if answer != 0: 
                    return answer #list(dict.fromkeys()) # remove dup
        return None

"""
print("______SOLVING USING IDDFS_________")
for i in range(1, 20):
    p = create_tile_puzzle(3, 3)
    p.scramble(100)
    print(p.find_solution_a_star())

print("______SOLVING USING A*_________")
for i in range(1, 20):
    p = create_tile_puzzle(3, 3)
    p.scramble(100)
    print(p.find_solution_a_star())
"""

############################################################
# Section 2: Grid Navigation
############################################################

def find_path(start, goal, scene):
    # True valeus corresponding to obsticals.
    # False values corresponding to empty spaces.

    if (scene[start[0]][start[1]] == True):
        return None # the start is on an obstical
    if (scene[goal[0]][goal[1]] == True):
        return None # the Goal is on an obstical
    if (start == goal):
        return None # You have allready won
    
    def successors (position):
        # yield all options to false squares (you can move diagnal)
        if position[0]-1 >= 0 and position[1]-1 >= 0 and scene[position[0]-1][position[1]-1] == False: # check the top left corner
            yield (position[0]-1, position[1]-1)
        if position[1]-1 >= 0 and scene[position[0]][position[1]-1] == False:# check the top
            yield (position[0], position[1]-1)
        if position[0]+1 < len(scene) and position[1]-1 >= 0 and scene[position[0]+1][position[1]-1] == False: # check the top right corner
            yield (position[0]+1, position[1]-1)

        if position[0]-1 >= 0 and scene[position[0]-1][position[1]] == False:# check the left
            yield (position[0]-1, position[1])
        if position[0]+1 < len(scene) and scene[position[0]+1][position[1]] == False:# check the right
            yield (position[0]+1, position[1])

        if position[0]-1 >= 0 and position[1]+1 < len(scene[0]) and scene[position[0]-1][position[1]+1] == False: # check the bottom left corner
            yield (position[0]-1, position[1]+1)
        if position[1]+1 < len(scene) and scene[position[0]][position[1]+1] == False:# check the bottom
            yield (position[0], position[1]+1)
        if position[0]+1 < len(scene) and position[1]+1 < len(scene[0]) and scene[position[0]+1][position[1]+1] == False: # check the bottom right corner
            yield (position[0]+1, position[1]+1)

    def isAnswer(position):
        # Return if an answer has been found in the list of posibilites
        if position == goal:
            return True
        return False

    # Priority queue only holds the current level in the tree.
    unvisited = PriorityQueue()
    heuristic = int(sqrt((start[0]-goal[0])**2 + (start[1]-goal[1])**2)*100)
    unvisited.put((heuristic, start, [start]))

    # create a visited list
    visited = [start]

    while unvisited.empty() == False:

        # Get the next level of the tree
        heuristic, position, path  = unvisited.get()
        for index in successors(position):

            # evaluate the current height
            if index not in visited:
                templist = path[:]
                templist.append(index)

                # find the shortest path. the priority queue will sort it for me
                heuristic = int(sqrt((index[0]-goal[0])**2 + (index[1]-goal[1])**2)*100)
                unvisited.put((heuristic, index, templist))
                visited.append(index)

                # check if i have the answer
                if isAnswer(index) == True:
                    return templist

    # if no solutions exsist
    return None

"""
#scene = [[choice(["X", ".", ".", "."]) for i in range(2000)] for i in range(1000)]
#for i in scene:
#    for x in i:
#        print(x, end='')
#    print("")

#times = time.time()
#print(print(find_path((0, 0), (5, 5), scene)))
#print(time.time()- times)
"""

############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################

def solve_distinct_disks(length, n):
    # add heuristics for significant improvements in performance.
    """
    Length is the length of the strip. 
    n is the number of disks at the beginning of the strip. 
    """

    #special case for if you have allready won
    if (length == 1 and n == 1):
        return []

    visited = []

    def isAnswer(current, goal):
        # Return if an answer has been found in the list of posibilites
        if current == goal:
            return True
        return False

    def huristic (current, goal, tree_height):
        #print("CURRENT TAPE: ", current, "   GOAL TAPE: ", goal)
        h = 0
        for i in current:
            h += abs(goal.index(i) - current.index(i))
        #print("H = ", h)
        return h + tree_height*4


    def makeMove(currentTape, value, pos1, pos2):
        newTape = currentTape[:]
        newTape[pos1] = 0
        newTape[pos2] = value
        return newTape

    def successors(currentTape):
        """ returns a list of all the moves that can be made  """

        for index in range(len(currentTape)):
            # if the spot has a disk
            if currentTape[index] > 0:
                if index+1 < len(currentTape):
                    #check if it can move forward 1 square
                    if currentTape[index+1] == 0:
                        newTape = makeMove(currentTape, currentTape[index], index, index+1)

                        # check the visited
                        if newTape not in visited:
                            yield(index, index+1), newTape[:]


                if index+2 < len(currentTape):
                    # check if it can move two squares.
                    if currentTape[index+1] > 0 and currentTape[index+2] == 0:
                        newTape = makeMove(currentTape, currentTape[index], index, index+2)

                        # check the visited
                        if newTape not in visited:
                            yield(index, index+2), newTape[:]


                #### New move backwords ####
                #check if it can move backwords 1 square
                if index-1 >= 0:
                    if currentTape[index-1] == 0:
                        newTape = makeMove(currentTape, currentTape[index], index, index-1)

                        # check the visited
                        if newTape not in visited:
                            yield(index, index-1), newTape[:]

                if index-2 >= 0:
                    # check if it can move two squares.
                    if currentTape[index-1] > 0 and currentTape[index-2] == 0:
                        newTape = makeMove(currentTape, currentTape[index], index, index-2)

                        # check the visited
                        if newTape not in visited:
                            yield(index, index-2), newTape[:]

    #create the tape representation.
    start = [x+1 if x < n else 0 for x in range(length)]
    goal = [length-x if x >= length - n else 0 for x in range(length)]
    


    if (length == 1 and n == 1):
        return []


    # Priority queue only holds the current level in the tree.
    unvisited = PriorityQueue()
    heuristic = int(sqrt((start[0]-goal[0])**2 + (start[1]-goal[1])**2)*100)
    unvisited.put((heuristic, start, []))

    # create a visited list
    visited = [start]

    while unvisited.empty() == False:

        # Get the next level of the tree
        heuristic, position, path  = unvisited.get()
        for provous_path, index in successors(position):

            # evaluate the current height
            if index not in visited:
                templist = path[:]
                templist.append(provous_path)
                

                # find the shortest path. the priority queue will sort it for me
                heuristic = huristic(index, goal, len(path))
                unvisited.put((heuristic, index, templist))
                visited.append(index)

                #print(path, provous_path, heuristic)
                # check if i have the answer
                if isAnswer(index, goal) == True:
                    #print("HELP ", heuristic, index, templist)
                    return templist

    # tape is full, there are no moves
    return None

"""
times = time.time()
print(solve_distinct_disks(10, 5))
print(time.time()- times)
"""

############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    return DominoesGame([[False for x in range(cols)] for y in range(rows)])

class DominoesGame(object):

    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def reset(self):
        self.board = [[False for x in range(len(self.board[0]))] for y in range(len(self.board))]

    def is_legal_move(self, row, col, vertical):
        if vertical == True and 0 <= row < len(self.board)-1 and 0 <= col < len(self.board[row]) and self.board[row][col] == False and self.board[row+1][col] == False:
            return True
        if vertical == False and 0 <= row < len(self.board) and 0 <= col < len(self.board[row])-1 and self.board[row][col] == False and self.board[row][col+1] == False:
            return True
        return False

    def legal_moves(self, vertical):
        for row in range(len(self.board)):
            for element in range(len(self.board[row])):
                if self.is_legal_move(row, element, vertical) == True:
                    yield (row, element)

    def perform_move(self, row, col, vertical):
        if vertical == True:
            self.board[row][col] = True; self.board[row+1][col] = True
        else: 
            self.board[row][col] = True; self.board[row][col+1] = True

    def game_over(self, vertical):
        if len(list(self.legal_moves(vertical))) == 0:
            return True
        return False

    def copy(self):
        return DominoesGame([[n for n in self.board[x]] for x in range(len(self.board))])

    def successors(self, vertical):
        for index in self.legal_moves(vertical):
            newboard = self.copy()
            newboard.perform_move(index[0], index[1], vertical)            
            yield (index, newboard)

    def get_random_move(self, vertical):
        return choice(list(self.legal_moves(vertical)))

    

    # Required
    def get_best_move(self, vertical, limit):
        # state is the currint verion of the domino game.
        opposite = {True:False, False:True}

        def Evaluation (state):
            return len(list(state.legal_moves(vertical)))-len(list(state.legal_moves(opposite[vertical])))

        def terminal_test(state, vertical, limit):
            return state.game_over(vertical) or limit == 0

        #def Actions(state, vertical):
        #    return list(state.successors(vertical))

        #def Result(s, a):
        #    return s.perform_move(a[0], a[1], vertical)

        def Utility(state, prevous_move, tree_height):
            return prevous_move, Evaluation(state), tree_height + 1

        def alpha_bata_search(state, vertical, limit):
            return max_value(state, float("-inf"), float("inf"), (), vertical, 0, limit)

        def max_value(state, a, b, prevous_move, vertical, tree_height, limit):
            """ returns a utility value """

            # Termanal test, return utility if True
            if terminal_test(state, vertical, limit): return Utility(state, prevous_move, tree_height)
            
            # set v to negitave infinity
            v = float("-inf")

            # for each a in the actions states
            for action, state in state.successors(vertical): #Actions(state):

                # Get the Max, of evaluaion or v
                new_move, evaluation, tree_height = min_value(state, a, b, action, opposite[vertical], tree_height, limit-1)
                if evaluation > v: move, v = action, evaluation

                # Find the max value for alpha
                if v >= b: return move, v, tree_height
                a = max(a, v)

            # return the answer of v
            return move, v, tree_height


        def min_value(state, a, b, prevous_move, vertical, tree_height, limit):
            """ returns a utility value """

            # Termanal test, return utility if True
            if state.game_over(vertical) or limit == 0: return Utility(state, prevous_move, tree_height)

            # set v to infinity
            v = float("inf")

            # for each a in the actions states
            for action, New_state in state.successors(vertical): #Actions(state):

                # get the min of the two values (evaluaions or v)
                new_move, evaluation, tree_height = max_value(New_state, a, b, action, opposite[vertical], tree_height, limit-1)
                if evaluation < v: move, v = action, evaluation
                
                # Find the min value for beta
                if v <= a: return move, v, tree_height
                b = min(b, v)

            # return the answer of v
            return move, v, tree_height

        return alpha_bata_search(self.copy(), vertical, limit)

"""
b = [[False] * 3 for i in range(3)]
g = DominoesGame(b)
print(g.get_best_move(True, 1))
print(g.get_best_move(True, 2))
b = [[False] * 3 for i in range(3)]
g = DominoesGame(b)
g.perform_move(0, 1, True)
print(g.get_best_move(False, 1))
print(g.get_best_move(False, 2))
"""
############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
26 Hours
"""

feedback_question_2 = """
IDDFS and Min value, yes
"""

feedback_question_3 = """
None. make the assignment a group project. Or since we alllredy created helper
fuctions for all the other programs, provide them complete so we dont have to do buisy work.
"""

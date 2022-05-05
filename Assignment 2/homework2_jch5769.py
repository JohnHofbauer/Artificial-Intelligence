############################################################
# CMPSC 442: Homework 2
############################################################

student_name = "John Hofbauer"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

from random import random, randint
from math import factorial
import time


############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    # returs the places a queen can be places using statisics. (n chose k)
    # where n is n*n, and k is n
    return int(factorial(n * n) / (factorial(n) * factorial(n * n - n)))



def num_placements_one_per_row(n):
    # there are n^n placemnts of queens on a board with replacemnt
    return n ** n
    # I dont know why we are doing stat in a computer science class. smh


def n_queens_valid(board):
    # If i represents the Columb it is not possoble to have a queen is the same Columb, with this board represntation.
    # Keep track of the row, so that no two are the same. 
    # some how add the diaganal, and update it every check to the right. 
    checker = []
    for index in range(len(board)):
        if board[index] not in checker:  # check the row.

            for checked in range(len(checker)):  # Check the diaganlas of the prevouse queens (BOTH DIAGALS)
                if board[index] == checker[checked] + index - checked or board[index] == checker[checked] - index + checked:
                    return False  # Queen can attack another
            checker.append(board[index])
        else:
            return False
    return True  # No queen can attack another


def n_queens_solutions(n):
    '''
    This is a version of the A* algorithm. 
    '''
    #starting list
    listd = [[x] for x in range(n)]

    # Repeate for the board size
    for i in range(n-1):
        newList = []

        # add all posible values to the set of accepted states.
        for i in range(n): 
            

            for index in listd:

                list4 = index[:]
                list4.append(i)

                # Check if it is vallid
                if n_queens_valid(list4) == True:
                    newList.append(list4[:])

        # Set the new accepted states.
        listd = newList


    # Yields the answers to the user.
    for i in listd:
        yield i[:]



############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def perform_move(self, rows, columns):
        if type(rows) == type(tuple()):
            rows = rows[0]
        if type(columns) == type(tuple()):
            columns = columns[0]
        def flip(n, m):
            
                
            #print("n: " + str(n) + "  columns: " + str(columns))
            #print(columns + m )
                
            if 0 <= rows + n < len(self.board) and 0 <= columns + m < len(self.board[0]):  # Check for out of range
                #print("row = " + str(row + n) + "    Col = " + str(col + m))
                if self.board[rows + n][columns + m]:
                    self.board[rows + n][columns + m] = False
                else:
                    self.board[rows + n][columns + m] = True
            else:
                pass  # Out of range exception

        flip(0, 0)  # Center
        #print("Center: " + str(self.get_board()))
        flip(0, 1)  # Right
        #print("Right: " + str(self.get_board()))
        flip(0, -1)  # Left
        #print("Left: " + str(self.get_board()))
        flip(1, 0)  # bottom
        #print("bottom: " + str(self.get_board()))
        flip(-1, 0)  # Top
        #print("top: " + str(self.get_board()))

    def scramble(self):
        """
        Calls Reform_move on every location of the board, with a probability of .5, that the
        result will be true.
        """
        for rows in range(len(self.board)):
            for columns in range(len(self.board[0])):
                if random() < 0.5:
                    self.perform_move(rows, columns)
                    #print("SCRAMBLING: " + str(rows) + "     " + str (columns))

    def is_solved(self):
        for rows in self.board:
            if True in rows:
                return False
        return True

    def copy(self):
        """ copy the board to a new object and return it. """
        #print(self.get_board())
        return LightsOutPuzzle([[n for n in self.board[x]] for x in range(len(self.board))])  # DEEEEEEEP copy!

    def successors(self):
        #print("row = " + str(len(self.board)) + "    Col = " + str(len(self.board[0])))
        for rows in range(len(self.board)):
            #print(rows)
            for columns in range(len(self.board[0])):
                #print((rows, columns), self.board)
                self.perform_move(rows, columns)
                #print(self.get_board())
                yield (rows, columns), self.copy()
                self.perform_move(rows, columns)

    def find_solution(self):
        """
        Finds the solution to the puzzle using breadth-first graph search.
        Do not add puzzle states if they have already been visited or are currently.
        If not solvabe return None

        find the successors, of every posibility, that has not allready been checked.
        """

        # Gets the posibilites
        self.steps = []
        self.visited = []
        self.successorsFound = 1 # this starts off on.



        def nextLevel(prevouse = ()):
            #print("Origial: " + str(self.get_board()))
            # Find the successors.
            for moves, new_board in self.successors(): 
                #print("visited" + str(visited))
                
                # make sure they were not visited.
                if new_board.get_board() not in self.visited: 
                    #print("successors: " + str(moves) + str(new_board.get_board()))
                    
                    self.successorsFound = 1

                    # Populete the lists.
                    if len(prevouse) > 0:
                        #### Formating lists cause that's what i enjoy spending hours on.
                        newnewlist = prevouse
                        if type(newnewlist) == type(tuple()):
                            newnewlist = [prevouse[:]]
                            newnewlist.append(moves)
                        else: 
                            newnewlist = prevouse[:]
                            newnewlist.append(moves)
                        self.steps.append((newnewlist, self.copy().get_board()))
                    else:
                        self.steps.append((moves, self.copy().get_board()))
                    self.visited.append(self.copy().get_board())


        def checkThem(index):
            """
            Check for all false in the steps list.
            """
            faseBord = [[False for n in range(len(self.board[x]))] for x in range(len(self.board))]
            
            
            # Return if an answer has been found in the list of posibilites
            if faseBord == self.steps[index][1]:
                #print("DONE")
                return self.steps[index][0]
            else:
                return 0


        # special case for only one move
        nextLevel()

        for index in range(len(self.steps)):
            answer = checkThem(index)
            if answer != 0: 
                return [answer]

        # Use a FOUND SUCCESSSER verable to know if i need to keep checking.
        while self.successorsFound == 1:
            self.successorsFound = 0
            #print("__________Gettign succ____________")
            for index in range(len(self.steps)):
                # Go through the steps list replacing them with the next height. adding nxn entries

                # save the current board
                currentBoard = self.copy().get_board()
                
                self.board = self.steps[index][1] # Set the board
                #print("Origial Stored: " + str(self.steps[index][1]))
                #print("Origial After set: " + str(self.get_board()))
                nextLevel(self.steps[index][0])

                self.board = currentBoard


            for index in range(len(self.steps)): # only check what hasn't been checked before
                answer = checkThem(index)
                if answer != 0: 
                    return answer #list(dict.fromkeys()) # remove dup



        


        return None


def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False for n in range(cols)] for x in range(rows)])

'''
for i in range(1, 20):
    p = create_puzzle(randint(2,4), randint(2,4))
    p.scramble()
    print("SOLUTION: " + str(p.find_solution()))
'''

############################################################
# Section 3: Linear Disk Movement
############################################################

def solve_identical_disks(length, n):
    """
    Length is the length of the strip. 
    n is the number of disks at the beginning of the strip. 
    """
    #create the tape representation.
    tape = [1 if x < n else 0 for x in range(length)]
    goal = [1 if x >= length - n else 0 for x in range(length)]

    #print("Given Tape: " + str(tape))
    #print("Goal Tape: " + str(goal))
    successorsFound = 1
    #print (tape)
    answer = []


    posibilites = []
    visited = []

    def makeMove(currentTape, pos1, pos2):
        newTape = currentTape[:]
        newTape[pos1] = 0
        newTape[pos2] = 1
        return newTape

    def findSuccessors(prevouse = (), currentTape = tape):
        """
        returns a list of all the moves that can be made
        """
        successorsfound = 0
        #print("Origial: " + str(currentTape))
        for index in range(len(currentTape)):

            # if the spot has a disk
            if currentTape[index] == 1:
                if index+1 >= len(currentTape):
                    break
                #check if it can move forward 1 square
                if currentTape[index+1] == 0:
                    
                    #print(str((index, index+1))) # The move that can be taken.

                    newTape = makeMove(currentTape, index, index+1)
                    
                    #print(str(newTape)) # show the move taking place

                    # check the visited
                    if newTape not in visited:
                        #print("successor: " + str(newTape))
                        successorsfound = 1
                        # Append the move to the list of posibilites
                        visited.append(newTape[:])
                        if prevouse == ():
                            posibilites.append([[(index, index+1)], newTape[:]])
                        else:
                            newnewlist = prevouse[:]
                            newnewlist.append((index, index+1))
                            posibilites.append([newnewlist, newTape[:]])

                if index+2 >= len(currentTape):
                    break
                # check if it can move two squares.
                if currentTape[index+1] == 1 and currentTape[index+2] == 0:
                    
                    #print(str((index, index+2)))
                    newTape = makeMove(currentTape, index, index+2)
                    #print(str(newTape)) # show the move taking place 
                    

                    # check the visited
                    if newTape not in visited:
                        #print("successor: " + str(newTape))
                        successorsfound = 1
                        # Append the move to the list of posibilites
                        visited.append(newTape[:])
                        if prevouse == ():
                            posibilites.append([[(index, index+2)], newTape[:]])
                        else:
                            newnewlist = prevouse[:]
                            newnewlist.append((index, index+2))
                            posibilites.append([newnewlist, newTape[:]])

        return successorsfound
        



    findSuccessors()

    def checkSuccessors():
        for index in posibilites:
            
            #print(goal)
            #print(index[1] == goal)
            #print(index[1])
            #print(goal)
            if index[1] == goal:
                #print("The Answer Has Been Found: " + str(index[0]))
                return index[0]

        return []
    # Check Successsors
    answer = checkSuccessors()

    # finish when the first answer is found
    if answer != []:
        #print("DONE: " + str(answer))
        return answer
    
    # for when It takes more than one pass.
    while successorsFound == 1:
        

        successorsFound = 0
        #print("testing" + str(posibilites))
        for index in range(len(posibilites)):
            succ = 0 
            #print("testing" + str(posibilites[index][1]))
            succ = findSuccessors(posibilites[index][0], posibilites[index][1])

            # make a gate, if there is one succ, then there are successors
            if succ == 1:
                successorsFound = 1

        #print("successorsfound: " + str(successorsFound))
        #print("______posibilites_______")
        #for i in posibilites:
        #    print(i)
        #print("______visited_______")
        #for i in visited:
        #    print(i)
        # Check Successsors
        answer = checkSuccessors()

        # finish when the first answer is found
        if answer != []:
            #print("DONE: " + str(answer))
            return answer

    # Return a list of tuples

    # tape is full, there are no moves
    return None


def solve_distinct_disks(length, n):
    """
    Length is the length of the strip. 
    n is the number of disks at the beginning of the strip. 
    """
    #create the tape representation.
    tape = [x+1 if x < n else 0 for x in range(length)]
    goal = [length-x if x >= length - n else 0 for x in range(length)]

    #print("Given Tape: " + str(tape))
    #print("Goal Tape: " + str(goal))
    successorsFound = 1
    #print (tape)
    answer = []


    posibilites = []
    visited = []

    def makeMove(currentTape, value, pos1, pos2):
        newTape = currentTape[:]
        newTape[pos1] = 0
        newTape[pos2] = value
        return newTape

    def findSuccessors(prevouse = (), currentTape = tape):
        """
        returns a list of all the moves that can be made
        """
        successorsfound = 0
        #print("Origial: " + str(currentTape))
        for index in range(len(currentTape)):

            # if the spot has a disk
            if currentTape[index] > 0:
                if index+1 < len(currentTape):
                    #check if it can move forward 1 square
                    if currentTape[index+1] == 0:
                        
                        #print(str((index, index+1))) # The move that can be taken.

                        newTape = makeMove(currentTape, currentTape[index], index, index+1)
                        
                        #print(str(newTape)) # show the move taking place

                        # check the visited
                        if newTape not in visited:
                            #print("successor: " + str(newTape))
                            successorsfound = 1
                            # Append the move to the list of posibilites
                            visited.append(newTape[:])
                            if prevouse == ():
                                posibilites.append([[(index, index+1)], newTape[:]])
                            else:
                                newnewlist = prevouse[:]
                                newnewlist.append((index, index+1))
                                posibilites.append([newnewlist, newTape[:]])

                if index+2 < len(currentTape):
                    # check if it can move two squares.
                    if currentTape[index+1] > 0 and currentTape[index+2] == 0:
                        
                        #print(str((index, index+2)))
                        newTape = makeMove(currentTape, currentTape[index], index, index+2)
                        #print(str(newTape)) # show the move taking place 
                        

                        # check the visited
                        if newTape not in visited:
                            #print("successor: " + str(newTape))
                            successorsfound = 1
                            # Append the move to the list of posibilites
                            visited.append(newTape[:])
                            if prevouse == ():
                                posibilites.append([[(index, index+2)], newTape[:]])
                            else:
                                newnewlist = prevouse[:]
                                newnewlist.append((index, index+2))
                                posibilites.append([newnewlist, newTape[:]])


                #### New move backwords ####
                #check if it can move backwords 1 square
                if index-1 >= 0:
                    if currentTape[index-1] == 0:
                        
                        #print(str((index, index-1))) # The move that can be taken.

                        newTape = makeMove(currentTape, currentTape[index], index, index-1)
                        
                        #print(str(newTape)) # show the move taking place

                        # check the visited
                        if newTape not in visited:
                            #print("successor: " + str(newTape))
                            successorsfound = 1
                            # Append the move to the list of posibilites
                            visited.append(newTape[:])
                            if prevouse == ():
                                posibilites.append([[(index, index-1)], newTape[:]])
                            else:
                                newnewlist = prevouse[:]
                                newnewlist.append((index, index-1))
                                posibilites.append([newnewlist, newTape[:]])

                if index-2 >= 0:
                    #print("INDEX: " + str(index-2))
                    # check if it can move two squares.
                    if currentTape[index-1] > 0 and currentTape[index-2] == 0:
                        
                        #print(str((index, index-2)))
                        newTape = makeMove(currentTape, currentTape[index], index, index-2)
                        #print(str(newTape)) # show the move taking place 
                        

                        # check the visited
                        if newTape not in visited:
                            #print("successor: " + str(newTape))
                            successorsfound = 1
                            # Append the move to the list of posibilites
                            visited.append(newTape[:])
                            if prevouse == ():
                                posibilites.append([[(index, index-2)], newTape[:]])
                            else:
                                newnewlist = prevouse[:]
                                newnewlist.append((index, index-2))
                                posibilites.append([newnewlist, newTape[:]])

        return successorsfound
        



    findSuccessors()

    def checkSuccessors():
        for index in posibilites:
            
            #print(goal)
            #print(index[1] == goal)
            #print(index[1])
            #print(goal)
            if index[1] == goal:
                #print("The Answer Has Been Found: " + str(index[0]))
                return index[0]

        return []
    # Check Successsors
    answer = checkSuccessors()

    # finish when the first answer is found
    if answer != []:
        #print("DONE: " + str(answer))
        return answer
    
    # for when It takes more than one pass.
    while successorsFound == 1:
        

        successorsFound = 0
        #print("testing" + str(posibilites))
        for index in range(len(posibilites)):
            succ = 0 
            #print("testing" + str(posibilites[index][1]))
            succ = findSuccessors(posibilites[index][0], posibilites[index][1])

            # make a gate, if there is one succ, then there are successors
            if succ == 1:
                successorsFound = 1

        #print("successorsfound: " + str(successorsFound))
        #print("______posibilites_______")
        #for i in posibilites:
        #    print(i)
        #print("______visited_______")
        #for i in visited:
        #    print(i)
        # Check Successsors
        answer = checkSuccessors()

        # finish when the first answer is found
        if answer != []:
            #print("DONE: " + str(answer))
            return answer

    # Return a list of tuples

    # tape is full, there are no moves
    return None

times = time.time()
print(solve_distinct_disks(10, 5))
print(time.time()- times)

############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
20.5 Hours
"""

feedback_question_2 = """
half of the time I was know that my lists where not getting Deepcopyed becuse there is no sytax error
only data error.
"""

feedback_question_3 = """
I like the GUI for the lights, that was nice. 
I would have liked a better stucture, like (VERY HIGH) level of sudo code. this could outline helper 
functions. Otherwise I feel like im stumbling in the dark. Also a drawing, or diagram for the disks 
quesiton would have been helpfull
"""

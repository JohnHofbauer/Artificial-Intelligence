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


############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    # returs the places a queen can be places using statisics. (n chose k)
    # where n is n*n, and k is n
    return factorial(n * n) / (factorial(n) * factorial(n * n - n))



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
                if board[index] == checker[checked] + index - checked or board[index] == checker[                 checked] - index + checked:
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

'''
print(n_queens_valid([0, 1]))
print(n_queens_valid([1, 1]))
print(n_queens_valid([1, 0]))
print(n_queens_valid([1, 3, 2]))
print(n_queens_valid([1, 3, 5, 0, 2, 4]))
print(n_queens_valid([1, 3, 0, 2, 4, 5]))
print(list(n_queens_solutions(6)))
print(len(list(n_queens_solutions(8))))
'''

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
                #print("successors: " + str(moves) + str(new_board.get_board()))
                # make sure they were not visited.
                if new_board.get_board() not in self.visited: 
                    
                    self.successorsFound = 1

                    # Populete the lists.
                    if len(prevouse) > 0:
                        #### Formating lists cause that's what i enjoy spending hours on.
                        newnewlist = prevouse
                        if type(newnewlist) == type(tuple()):
                            newnewlist = [prevouse[:]]
                            newnewlist.append(moves)
                        else: 
                            newnewlist = prevouse
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
                #print(steps[index][0][-2])
                #print(self.steps[index])
                #print("prevous: " + str(self.get_board()))
                #self.perform_move(self.steps[index][0][-1], self.steps[index][0][-1])

                # save the current board
                currentBoard = self.copy().get_board()
                
                self.board = self.steps[index][1] # Set the board
                #print("Origial Stored: " + str(self.steps[index][1]))
                #print("Origial After set: " + str(self.get_board()))
                nextLevel(self.steps[index][0])

                self.board = currentBoard

                #path.append([steps[index][0][0]])
                

                #self.perform_move(self.steps[index][0][-1], self.steps[index][0][-1]) # preform the last move from the list.
            '''
            print("SUC FOND: " + str(self.successorsFound == 1))

            print("__________STEPS____________")
            for i in self.steps:
                print(i)
            print("__________VISITED____________")
            for i in self.visited:
                print(i)
            '''

            for index in range(len(self.steps)): # only check what hasn't been checked before
                answer = checkThem(index)
                if answer != 0: 
                    return list(dict.fromkeys(answer)) # remove dup



        


        return None


def create_puzzle(rows, cols):
    return LightsOutPuzzle([[False for n in range(cols)] for x in range(rows)])

"""
b = [[True, False], [False, True]]
p = LightsOutPuzzle(b)
print(p.get_board())
b = [[True, True], [True, True]]
p = LightsOutPuzzle(b)
print(p.get_board())
p = create_puzzle(2, 2)
print(p.get_board())
p = create_puzzle(2, 3)
print(p.get_board())
p = create_puzzle(3, 3)
p.perform_move(1, 1)
print(p.get_board())

for i in range(1, 20):
	p = create_puzzle(4, 4)
	p.scramble()
	print(p.is_solved())


b = [[True, False], [False, True]]
p = LightsOutPuzzle(b)
print(p.is_solved())
b = [[False, False], [False, False]]
p = LightsOutPuzzle(b)
print(p.is_solved())

print("__________________")
p = create_puzzle(3, 3)
p2 = p.copy()
print(p.get_board() == p2.get_board())

p = create_puzzle(3, 3)
p2 = p.copy()
p.perform_move(1, 1)
print(p.get_board() == p2.get_board())

print("_7._________________")
p = create_puzzle(2, 2)
for move, new_p in p.successors():
    print(move, new_p.get_board())

for i in range(2, 6):
    p = create_puzzle(i, i + 1)
    print(len(list(p.successors())))



p = create_puzzle(2, 3)
for row in range(2):
    for col in range(3):
        p.perform_move(row, col)
"""

for i in range(1, 20):
    p = create_puzzle(randint(2,3), randint(2,3))

    p.scramble()



    print("SOLUTION: " + str(p.find_solution()))

    #assert(p.find_solution() == None)



#print(p.find_solution())

#print("_8._________________")
#b = [[False, False, False], [False, False, False]]
#b[0][0] = True
#p = LightsOutPuzzle(b)
#print(p.get_board())
#for move, new_p in p.successors():
    #print(move, new_p.get_board())

#print(p.get_board())
#print(p.find_solution())
#print(p.find_solution() is None)

############################################################
# Section 3: Linear Disk Movement
############################################################

def solve_identical_disks(length, n):
    pass


def solve_distinct_disks(length, n):
    pass


############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

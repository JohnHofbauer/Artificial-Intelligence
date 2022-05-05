############################################################
# CMPSC 442: Homework 1
############################################################

student_name = "John Hofbauer."

############################################################
# Section 1: Working with Lists
############################################################


def extract_and_apply(l, p, f):
    return [f(x) for x in l if p(x)] 
    # [ans, reference, condition]


def concatenate(seqs):
    # for every element in the list add every sub element into a new list.
    return [elements for lists in seqs for elements in lists]
    # [ans, reference, rule]


def transpose(matrix):
    # For the first element in every row, make the new column for every row.
    return [[matrix[y][x] for y in range(len(matrix))] for x in range(len(matrix[0]))]
    # [ans, reference, rule]

############################################################
# Section 2: Sequence Slicing
############################################################


def copy(seq):
    return seq[:]
    # [start, end, step] copy of seq


def all_but_last(seq):
    return seq[:-1]
    # [start, end, step] copy minus last 


def every_other(seq):
    return seq[::2]
    # [start, end, step] copy of every other. step = 2


############################################################
# Section 3: Combinatorial Algorithms
############################################################


def prefixes(seq):
    newList = []
    newList2 = seq[:]
    for x in range(len(seq)+1):
        yield newList2[:x]
        #newList.append(newList2[:x])
    newList.append(seq[:])
    return newList


def suffixes(seq):
    newList = []
    newList2 = seq[:]
    for x in range(len(seq)+1):
        yield newList2[x:]
        #newList.append(newList2[x:])
    newList.append(seq[1:1])
    return newList


def slices(seq):
    newList = []
    for x in range(len(seq)):
        for y in range(len(seq)+1):
            if seq[x:y] != []:
                if seq[x:y] != '':
                    yield seq[x:y]

    return newList

############################################################
# Section 4: Text Processing
############################################################


def normalize(text):
    newText = text.lower().strip(' ')
    while '  ' in newText:
        newText = newText.replace('  ', ' ')
    return newText
    # lower() function


def no_vowels(text):
    return text.replace("a", "").replace("e", "").replace("i", "").replace("o", "").replace("u", "").replace("A", "")\
        .replace("E", "").replace("I", "").replace("O", "").replace("U", "")
    # remove() function


def digits_to_words(text):
    newString = ''
    for char in text:
        if char == '0': newString += ' zero '
        elif char == '1': newString += ' one '
        elif char == '2': newString += ' two '
        elif char == '3': newString += ' three '
        elif char == '4': newString += ' four '
        elif char == '5': newString += ' five '
        elif char == '6': newString += ' six '
        elif char == '7': newString += ' seven '
        elif char == '8': newString += ' eight '
        elif char == '9': newString += ' nine '
    while '  ' in newString:
        newString = newString.replace('  ', ' ')
    newString = newString.strip(' ')
    return newString


def to_mixed_case(name):
    return name.split("_", " ").capitalize().joined().strip(" ")

############################################################
# Section 5: Polynomials
############################################################

class Polynomial(object):

    def __init__(self, polynomial):
        self.poly = tuple(polynomial)

    def get_polynomial(self):
        return self.poly

    def __neg__(self):
        return Polynomial([(-x[0], x[1]) for x in self.poly])

    def __add__(self, other):
        return Polynomial([(x[0], x[1]) for x in self.poly] + [(x[0], x[1]) for x in other.poly])

    def __sub__(self, other):
        return Polynomial([(x[0], x[1]) for x in self.poly] + [(-x[0], x[1]) for x in other.poly])

    def __mul__(self, other):
        return Polynomial([(x[0]*y[0], x[1]+y[1]) for x in self.poly for y in other.poly])

    def __call__(self, x):
        return sum([y[0]*x**y[1] for y in self.poly])

    def simplify(self):
        newDict = {}
        for index in range(len(self.poly)):
            if self.poly[index][1] not in newDict:
                newDict[self.poly[index][1]] = self.poly[index][0]
            else:
                newDict[self.poly[index][1]] += self.poly[index][0]

        newList = [(newDict[x], x) for x in newDict]
        newList.sort(reverse=True, key=lambda y:y[1])

        for index in range(len(newList)):
            if index >= len(newList):
                break
            if newList[index][0] == 0:
                newList.pop(index)
                index -= 1

        self.poly = tuple(newList)
        return Polynomial(newList)


    def __str__(self):
        tempString = ''
        for index in range(len(self.poly)):

            # Specal case for the first poly in the string.
            if tempString == '':
                spacing = ""
            else:
                spacing = " "

            # every case i could think of!
            if self.poly[index][0] > 0 and self.poly[index][1] == 0:
                tempString += spacing + "+" + spacing + str(abs(self.poly[index][0]))
            elif self.poly[index][0] == 1 and self.poly[index][1] == 1:
                tempString += spacing + "+" + spacing + "x"
            elif self.poly[index][0] == 1 and abs(self.poly[index][1]) > 1:
                tempString += spacing + "+" + spacing + "x^" + str(self.poly[index][1])
            elif self.poly[index][0] > 1 and self.poly[index][1] == 1:
                tempString += spacing + "+" + spacing + str(abs(self.poly[index][0])) + "x"
            elif self.poly[index][0] == -1 and self.poly[index][1] == 1:
                tempString += spacing + "-" + spacing + "x"
            elif self.poly[index][0] == -1 and abs(self.poly[index][1]) > 1:
                tempString += spacing + "-" + spacing + "x^" + str(self.poly[index][1])
            elif self.poly[index][0] > 1 and self.poly[index][1] > 1:
                tempString += spacing + "+" + spacing + str(abs(self.poly[index][0])) + "x^" + str(self.poly[index][1])
            elif self.poly[index][0] < -1 and abs(self.poly[index][1]) > 1:
                tempString += spacing + "-" + spacing + str(abs(self.poly[index][0])) + "x^" + str(self.poly[index][1])
            elif self.poly[index][0] < -1 and self.poly[index][1] == 1:
                tempString += spacing + "-" + spacing + str(abs(self.poly[index][0])) + "x"
            elif self.poly[index][0] < 0 and self.poly[index][1] == 0:
                tempString += spacing + "-" + spacing + str(abs(self.poly[index][0]))
            elif self.poly[index][0] == 0 and self.poly[index][1] == 1:
                tempString += spacing + "+" + spacing + str(abs(self.poly[index][0])) + "x"
            elif self.poly[index][0] == 0 and self.poly[index][1] != 0:
                tempString += spacing + "+" + spacing + str(abs(self.poly[index][0])) + "x^" + str(self.poly[index][1])

        tempString = tempString.strip('+')  # no preceding positive sign.
        return tempString

############################################################
# Section 6: Feedback
############################################################

feedback_question_1 = """
15.5
"""

feedback_question_2 = """
section 5: '__mul__' function.
"""

feedback_question_3 = """
I believe including the test cases in the same .py file, would have made checking less strenuous.
"""

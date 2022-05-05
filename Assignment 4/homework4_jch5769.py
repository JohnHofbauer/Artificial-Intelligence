############################################################
# CMPSC 442: Homework 4
############################################################

student_name = "John_Hofbauer"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from itertools import product, permutations, combinations 
from collections import OrderedDict



############################################################
# Section 1: Propositional Logic
############################################################

class Expr(object):
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))

class Atom(Expr):
    def __init__(self, name):
        self.name = name
        self.hashable = name
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
    def __eq__(self, other):
        """ Return true, if self and other are same class and internal sturcture."""
        return type(self) == type(other) and self.hashable == other.hashable
    def __repr__(self):
        """ Return string of the object."""
        return "Atom(" + str(self.name) + ")"
    def __iter__(self):
        yield self
    def atom_names(self):
        """ Return a Set of the names that occur in the atoms """
        return (str(self.name))
    def evaluate(self, assignment):
        if assignment[str(self.name)] == True: return True # Case One: True = True
        if assignment[str(self.name)] == False: return False # Case One: True = True
    def to_cnf(self):
        return self

class Not(Expr):
    def __init__(self, arg):
        self.arg = arg
        self.hashable = arg
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
    def __eq__(self, other):
        """ Return true, if self and other are same class and internal sturcture."""
        return type(self) == type(other) and self.hashable == other.hashable
    def __repr__(self):
        """ Return string of the object."""
        return "Not(" + str(self.arg) + ")"
    def __iter__(self):
        yield self
    def atom_names(self):
        """ Return a Set of the names that occur in the atoms """
        print ("self.arg", type(self.arg), self.arg)
        return self.arg.atom_names()
    def evaluate(self, assignment):
        if self.arg.evaluate(assignment) == True: return False # Case One: True = False
        if self.arg.evaluate(assignment) == False: return True # Case One: False = True
    def to_cnf(self):
        # If there are two Not's, remove both
        if type(self.arg) == type(Not(Atom("Temp"))):
            return self.arg.arg.to_cnf()

        # Distribute the Not, then remove the top Not()
        if type(self.arg) == type(And()) or type(self.arg) == type(Or()):
            self.arg.applyNot()
            return self.arg.to_cnf()

        # if there is someting inside the not: proform cnf on the inside
        if type(self.arg) != type(Atom("Temp")):
            return Not(self.arg.to_cnf()).to_cnf()
        
        return self
        
class And(Expr):
    def __init__(self, *conjuncts):
        self.conjuncts = frozenset(conjuncts)
        self.hashable = self.conjuncts
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
    def __eq__(self, other):
        """ Return true, if self and other are same class and internal sturcture."""
        return type(self) == type(other) and self.hashable == other.hashable
    def __repr__(self):
        """ Return string of the object."""
        return "And("+ ", ".join([str(x) for x in self.conjuncts]) + ")"
    def __iter__(self):
        for i in self.conjuncts: 
            yield i 
    def atom_names(self):
        """ Return a Set of the names that occur in the atoms """
        newlist = []
        for index in self.conjuncts:
            if type(index) == type(Atom("temp1")) or type(index) == type(Not(Atom("temp1"))):
                newlist.append(index.atom_names())
            else:
                newlist.extend(list(index.atom_names()))
        return set(newlist)
    def evaluate(self, assignment):
        """ If any are false, return false. 
            Recursion, each part has its own evaluation methiod, so the combine is checked"""
        for index in [x for x in self.conjuncts]:
            if index.evaluate(assignment) == False: return False
        return True
    def applyNot(self): 
        newList = []
        for index in [x for x in self.conjuncts]: newList.append(Not(index))
        self.conjuncts = set(newList)
    def returnParts(self):
        return [i for i in self.conjuncts]
    def AddPart(self, other):
        newList = []
        for index in [x for x in self.conjuncts]: newList.append(index)
        newList.append(other)
        self.conjuncts = set(newList)
    def to_cnf(self):

        # combinnig And()
        tmps = []
        for index in self.conjuncts: 
            if type(index) == type(And()): tmps.extend(index)
            else: tmps.append(index)
        self.conjuncts = set(tmps)



        return self

class Or(Expr):
    def __init__(self, *disjuncts):
        self.disjuncts = frozenset(disjuncts)
        self.hashable = self.disjuncts
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
    def __eq__(self, other):
        """ Return true, if self and other are same class and internal sturcture."""
        return type(self) == type(other) and self.disjuncts == other.disjuncts
    def __repr__(self):
        """ Return string of the object."""
        return "Or("+ ", ".join([str(x) for x in self.disjuncts]) + ")"
    def __iter__(self):
        for i in self.disjuncts: yield i 
    def type(self):
        """ Return string of the object."""
        return type(self.disjuncts)
    def atom_names(self):
        """ Return a Set of the names that occur in the atoms """
        newlist = []
        for index in self.disjuncts:
            if type(index) == type(Atom("temp1")) or type(index) == type(Not(Atom("temp1"))):
                newlist.append(index.atom_names())
            else:
                newlist.extend(list(index.atom_names()))
        return set(newlist)
    def evaluate(self, assignment):
        """ If any are True, return True. 
            Recursion, each part has its own evaluation methiod, so the combine is checked"""
        for index in self.disjuncts:
            if index.evaluate(assignment) == True: return True
        return False
    def applyNot(self): 
        newList = []
        for index in [x for x in self.disjuncts]: newList.append(Not(index))
        self.disjuncts = set(newList)
    def to_cnf(self):

        # And() over Or() form: 
        found2 = [0, 0]
        things = []
        thing = []
        for index in self.disjuncts: 
            if type(index) == type(Not(Atom("Temp"))) and type(index.arg) == type(Or()): 
                found2[0] = 1
                things.extend([i for i in index.arg])
            if type(index) == type(Atom("Temp")): 
                found2[1] = 1
                thing.append(index)
        if found2 == [1, 1] and len(self.disjuncts) == 2:
            return And(Or(thing[0], Not(things[0])), Or(thing[0], Not(things[1])))

        # recursion for Not()'s found
        tmps = []
        for index in self.disjuncts: 
            if type(index) == type(Not(Atom("Temp"))): tmps.extend(index.to_cnf())
            else: tmps.append(index)
        self.disjuncts = set(tmps)

        # combinnig Or()
        tmps = []
        for index in self.disjuncts: 
            if type(index) == type(Or()): tmps.extend(index)
            else: tmps.append(index)
        self.disjuncts = set(tmps)

        # Check if it's clean
        clean = 1
        for index in self.disjuncts: 
            if type(index) == type(And()): clean = 0
        if clean == 1: return self
        
        # Disjunction of literals. 
        # Find the And() expreations, then get their expresions.
        # create a list of the combanations
        temp = (Or(*i) for i in list(product(*self.disjuncts)))

        # Change the class
        self.disjuncts = And(*temp)       

        # p \/ (q /\ a) =_ (p \/ q) /\ (p \/ a) 
        return self.disjuncts.to_cnf()

class Implies(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
    def __eq__(self, other):
        """ Return true, if self and other are same class and internal sturcture."""
        return type(self) == type(other) and self.hashable == other.hashable
    def __repr__(self):
        """ Return string of the object."""
        return "Implies("+ str(self.left) + ", " + str(self.right) +  ")"
    def atom_names(self):
        """ Return a Set of the names that occur in the atoms """
        newlist = []
        for index in [self.left, self.right]:
            if type(index) == type(Atom("temp1")) or type(index) == type(Not(Atom("temp1"))):
                newlist.append(index.atom_names())
            else:
                newlist.extend(list(index.atom_names()))
        return set(newlist)
        return set([index.atom_names() for index in [self.left, self.right]])
    def evaluate(self, assignment):
        if self.left.evaluate(assignment) == False and self.right.evaluate(assignment) == False: return True # Case One: False -> False = True
        if self.left.evaluate(assignment) == False and self.right.evaluate(assignment) == True: return True # Case Two: False -> True = True
        if self.left.evaluate(assignment) == True and self.right.evaluate(assignment) == False: return False # Case Three: True -> False = False
        if self.left.evaluate(assignment) == True and self.right.evaluate(assignment) == True: return True # Case Four: True -> True = True
    def applyNot(self): 
        self.left = Not(self.left)
        self.right = Not(self.right)
    def to_cnf(self):
        #p -> q =_ ~p \/ q
        self.left = Not(self.left).to_cnf()
        return Or(self.left.to_cnf(), self.right.to_cnf()).to_cnf()

class Iff(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.hashable = (left, right)
    def __hash__(self):
        return hash((type(self).__name__, self.hashable))
    def __eq__(self, other):
        """ Return true, if self and other are same class and internal sturcture."""
        return type(self) == type(other) and self.hashable == other.hashable
    def __repr__(self):
        """ Return string of the object."""
        return "IFF("+ str(self.left) + ", " + str(self.right) +  ")"
    def atom_names(self):
        """ Return a Set of the names that occur in the atoms """
        newlist = []
        for index in [self.left, self.right]:
            if type(index) == type(Atom("temp1")) or type(index) == type(Not(Atom("temp1"))):
                newlist.append(index.atom_names())
            else:
                newlist.extend(list(index.atom_names()))
        return set(newlist)
        return set([index.atom_names() for index in [self.left, self.right]])
    def evaluate(self, assignment):
        if self.left.evaluate(assignment) == False and self.right.evaluate(assignment) == False: return True # Case One: False -> False = True
        if self.left.evaluate(assignment) == False and self.right.evaluate(assignment) == True: return False # Case Two: False -> True = False
        if self.left.evaluate(assignment) == True and self.right.evaluate(assignment) == False: return False # Case Three: True -> False = False
        if self.left.evaluate(assignment) == True and self.right.evaluate(assignment) == True: return True # Case Four: True -> True = True
    def applyNot(self): 
        self.left = Not(self.left)
        self.right = Not(self.right)
    def to_cnf(self):
        # p <-> q =_ (p -> q) /\ (q -> p)
        # compleate the assignment atomicly so that the they do not effect eachother
        self.left, self.right = Implies(self.left, self.right).to_cnf(), Implies(self.right, self.left).to_cnf()
        return And(self.left, self.right)

def satisfying_assignments(expr):
    # A Python program to print all case of the expresion that are true
    atoms = list(expr.atom_names())

    # List of all the cases for true and false values.
    perm = [list(i) for i in product([False, True], repeat=len(atoms))]

    # list of all the posible tests
    tests = [{atoms[x]:i[x] for x in range(len(atoms))} for i in perm]

    # New list of all the outputs that have returned true
    output = [i for i in tests if (expr.evaluate(i)==True)]

    # Yeild the output
    for i in output:
        yield dict(OrderedDict(sorted(i.items()))).copy()
    
class KnowledgeBase(object):
    def __init__(self):
        self.object = object
        self.fact_set = ()
    def get_facts(self):
        return set(self.fact_set)
    def tell(self, expr):
        self.fact_set = set([i for i in self.fact_set] + [expr])

    def pl_resolution(self, KB, a):
        # using resuloution
        clauses = [And(i, Not(expr)) for i in self.fact_set]
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i+1, n)]

        templist = []
        while True:
            for Ci in clauses:
                for Cj in clauses:
                    resolves = satisfying_assignments(fact)
                    if len(resolves) == 0: return True
                    new = new + resolves
            if new in clauses: return False
            clauses = clauses + new

    def ask(self, expr):

        #return self.pl_resolution(self.fact_set, expr)

        equation = And(*self.fact_set)
        #print("New Expresion", And(*self.fact_set))

        posable_answers = list(satisfying_assignments(equation))
        print(posable_answers)

        Queeries = [i for i in expr.atom_names()]
        
        
        for i in Queeries:
            if i not in posable_answers[0]:
                #expr.evaluate() == True
                return False
            if posable_answers[0][i] == False:
                return False
        return True

    
       
"""
# 1
print(Atom("a") == Atom("a"))
print(Atom("a") == Atom("b"))
print(And(Atom("a"), Not(Atom("b"))) == And(Not(Atom("b")), Atom("a")))

# 2
a, b, c = map(Atom, "abc")
print(Implies(a, Iff(b, c)))
a, b, c = map(Atom, "abc")
print(And(a, Or(Not(b), c)))

# 3.
print(Atom("a").atom_names())
print(Not(Atom("a")).atom_names())

a, b, c = map(Atom, "abc")
expr = And(a, Implies(b, Iff(a, c)))
print(expr.atom_names())

# 4.
e = Implies(Atom("a"), Atom("b"))
print(e.evaluate({"a": False, "b": True}))
print(e.evaluate({"a": True, "b": False}))

a, b, c = map(Atom, "abc")
e = And(Not(a), Or(b, c))
print(e.evaluate({"a": False, "b": False, "c": True}))


#print("___own test cases_____")
#print("A is true: ", (a).evaluate({"a": True}))
#print("A is False: ", (a).evaluate({"a": False}))

#print("~A is true: ", Not(a).evaluate({"a": True}))
#print("~A is False: ", Not(a).evaluate({"a": False}))

#print("A is True (or) B is True: ", Or((a), (b)).evaluate({"a": True, "b": True}))
#print("A is True (or) B is True (or) C is True: ", Or((a), (b), (c)).evaluate({"a": True, "b": True, "c": True}))
#print("A is False (or) B is True: ", Or((a), (b)).evaluate({"a": False, "b": True}))
#print("A is True (or) B is False (or) C is True: ", Or((a), (b), (c)).evaluate({"a": True, "b": False, "c": True}))
#print("A is False (or) B is False (or) C is True: ", Or((a), (b), (c)).evaluate({"a": False, "b": False, "c": True}))
#print("A is False (or) B is False (or) C is False: ", Or((a), (b), (c)).evaluate({"a": False, "b": False, "c": False}))


#print("A is True (And) B is True (And) C is True: ", And((a), (b), (c)).evaluate({"a": True, "b": True, "c": True}))
#print("A is False (And) B is True: ", And((a), (b)).evaluate({"a": False, "b": True}))
#print("A is True (And) B is False (And) C is True: ", And((a), (b), (c)).evaluate({"a": True, "b": False, "c": True}))
#print("A is False (And) B is False (And) C is True: ", And((a), (b), (c)).evaluate({"a": False, "b": False, "c": True}))
#print("A is False (And) B is False (And) C is False: ", And((a), (b), (c)).evaluate({"a": False, "b": False, "c": False}))

print(Atom("a") == Not(Atom("b")))



#5 
e = Implies(Atom("a"), Atom("b"))
a = satisfying_assignments(e)
print(next(a))
print(next(a))
print(next(a))
e = Iff(Iff(Atom("a"), Atom("b")), Atom("c"))
print(list(satisfying_assignments(e)))

#6
print(Atom("a").to_cnf())

a, b, c = map(Atom, "abc")
print(Iff(a, Or(b, c)).to_cnf())

print(Or(Atom("a"), Atom("b")).to_cnf())

a, b, c, d = map(Atom, "abcd")
print(Or(And(a, b), And(c, d)).to_cnf())
"""

#print(Implies(Atom("a"), Atom("b")).to_cnf())
#print(Iff(Atom("a"), Atom("b")).to_cnf())
#print("testing Not", Not(And(Atom("a"), Atom("b"))).to_cnf())
#print("testing Not", Not(Or(Atom("a"), Atom("b"))).to_cnf())
#print("testing Not", Not(Not(Atom("a"))).to_cnf())

# remove or's in or's
#print(Or(Atom("a"), And(Atom("b"), Atom("C"))).to_cnf())
#print(Or(And(Atom("A"), Atom("B")), And(Atom("C"), Atom("D"))).to_cnf())
# remove and's in and's

# do compouding!! (DONT FORGET!!!!) ~ ima forget...
#print(Or(Atom("a"), Or(Atom("b"), Atom("C"))).to_cnf())

#print(Implies(Atom("b"), Atom("a")).to_cnf())

#print(Implies(Or(Atom("b"), Atom("c")), Atom("a")).to_cnf())
#print(Implies(Atom("a"), Or(Atom("b"), Atom("c"))).to_cnf())

#print(Not(Implies(a, b)).to_cnf())

#7 
"""
a, b, c = map(Atom, "abc")
kb = KnowledgeBase()
kb.tell(a)
kb.tell(Implies(a, b))
print(kb.get_facts())

print([kb.ask(x) for x in (a, b, c)])


a, b, c = map(Atom, "abc")
kb = KnowledgeBase()
kb.tell(Iff(a, Or(b, c)))
print([kb.ask(x) for x in (a, Not(a))])
print([kb.ask(x) for x in (b, Not(b))])
print([kb.ask(x) for x in (c, Not(c))])
"""


############################################################
# Section 2: Logic Puzzles
############################################################

# Puzzle 1

# Populate the knowledge base using statements of the form kb1.tell(...)
kb1 = KnowledgeBase()
kb1.tell(Implies(Atom("mythical"), Not(Atom("mortal"))))
kb1.tell(Implies(Not(Atom("mythical")), And(Atom("mortal"), Atom("mammal"))))
kb1.tell(Implies(Or(Not(Atom("mortal")), Atom("mammal")), Atom("horned")))
kb1.tell(Implies(Atom("mythical"), Not(Atom("mortal"))))
kb1.tell(Implies(Atom("horned"), Atom("magical")))


#knowledge1 = Implies(Atom("mythical"), Not(Atom("mortal")))
#knowledge2 = Implies(Not(Atom("mythical")), And(Atom("mortal"), Atom("mammal")))
#knowledge3 = Implies(Or(Not(Atom("mortal")), Atom("mammal")), Atom("horned"))
#knowledge4 = Implies(Atom("mythical"), Not(Atom("mortal")))
#knowledge5 = Implies(Atom("horned"), Atom("magical"))

#unicorn_constraints = And(knowledge1, knowledge2, knowledge3, knowledge4, knowledge5)
#for i in satisfying_assignments(unicorn_constraints):
#    print (i)

# Write an Expr for each query that should be asked of the knowledge base
#mythical_query = kb1.ask(Atom("mythical"))
#print(mythical_query)
#magical_query = And(Atom("mythical"),Atom("mortal"),Atom("mammal"),Atom("horned"),Atom("magical"))
#horned_query = And(Atom("mythical"),Atom("mortal"),Atom("mammal"),Atom("horned"),Atom("magical"))

# Record your answers as True or False; if you wish to use the above queries,
# they should not be run when this file is loaded
is_mythical = False
is_magical = True
is_horned = True

# Puzzle 2

# Write an Expr of the form And(...) encoding the constraints
cond1 = Implies(Or(Atom("m"), Atom("a")), Atom("j"))
cond2 = Implies(Not(Atom("m")), Atom("a"))
cond3 = Implies(Atom("a"), Not(Atom("j")))

party_constraints = And(cond1, cond2, cond3)

# Compute a list of the valid attendance scenarios using a call to
#print(list(satisfying_assignments(party_constraints)))
valid_scenarios = [{'Ann': False, 'John': True, 'Mary': True}]

# Write your answer to the question in the assignment
puzzle_2_question = """
There is only one solution, where
'Ann': Does not Come
'John': Does Come
'Mary': Does Come
"""

# Puzzle 3

# Populate the knowledge base using statements of the form kb3.tell(...)
# Atom("p1")
# Atom("e1")
# Atom("p2")
# Atom("e2")
# Atom("s1")
# Atom("s2")
# Knolage bases
signs = Iff(Not(Atom("s1")), Atom("s2"))
sign1 = Implies(Atom("p1"), Atom("e2"))
cond1 = And(Atom("s1"), sign1)
sign2 = And(Or(Atom("p1"), Atom("p2")), Or(Atom("e1"), Atom("e2")))
cond2 = And(Atom("s2"), sign2)

#facts = And(signs, cond1, cond2)
#for i in satisfying_assignments(facts):
#    print (i)

kb3 = KnowledgeBase()
kb3.tell(signs)
kb3.tell(sign1)
kb3.tell(sign2)
kb3.tell(cond1)
kb3.tell(cond2)

# Write your answer to the question in the assignment; the queries you make
# should not be run when this file is loaded
puzzle_3_question = """
room 2 has a prize and room 1 does not.
"""

# Puzzle 4

# Populate the knowledge base using statements of the form kb4.tell(...)
clark = And(Atom("ic"), And(Atom("ka"), Atom("kb")), Or(Not(Atom("ia")), Not(Atom("ib"))))
adams = And(Atom("ia"), Not(Atom("kc")))
brown = And(Atom("ib"), Not(Atom("kb")))

kb4 = KnowledgeBase()
kb4.tell(clark)
kb4.tell(adams)
kb4.tell(brown)

# Uncomment the line corresponding to the guilty suspect
# guilty_suspect = "Adams"
guilty_suspect = "Brown"
# guilty_suspect = "Clark"

# Describe the queries you made to ascertain your findings
puzzle_4_question = """
Brown is guilty
"""

############################################################
# Section 3: Feedback
############################################################

feedback_question_1 = """
50 hrs.
"""

feedback_question_2 = """
The whole thing.
"""

feedback_question_3 = """
None, I hated it.
"""

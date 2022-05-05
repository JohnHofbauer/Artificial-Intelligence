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


from sympy.logic.boolalg import *
from sympy.abc import *
from sympy import *



#print(to_cnf( ((c | b) >> a) & (a >> (c | b)) ))

oof1 = Implies(Atom("mythical"), Not(Atom("mortal")))
#oof2 = Implies(Not("mythical"), Or(Atom("mortal"), Atom("mammal")))
#oof3 = Implies(Or(Not(Atom("mortal")), Atom("mammal")), Atom("horned"))
#oof4 = Implies(Atom("mythical"), Not(Atom("mortal")))
#oof5 = Implies(Atom("horned"), Atom("magical"))


print (to_cnf(oof1))


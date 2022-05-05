############################################################
# CMPSC 442: Homework 6
############################################################

student_name = "John Hofbauer"

############################################################
# Imports
# What modules can I import?  -- collections, itertools, math, random, queue, email, os, re, string, copy, os
############################################################

# Include your imports here, if any are used.
import os
from collections import Counter
from math import log

############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    """
    Open the file with utf-8 encodigng, then create the list of tokens
    Close the file; Return a list of the tokens from the file. 
    """
    file = open(path, "r", encoding="utf-8")
    tokens = [[tuple(line.split("=")) for line in lines.rstrip('\n').split(" ")] for lines in file.readlines()]
    file.close(); return tokens

class Tagger(object):
	# The tagger is allways called after the load_corpus fuction, and input with the list-of-lists 
	# that it ouputs. 
    def __init__(self, sentences):
        self.sentences = sentences
        self.lengthOfTags = len([1 for sentence in sentences for i in sentence])

        # Dict of all the beginngin of sentence POS.
        self.initTagProb = dict(Counter([sentence[0][1] for sentence in sentences]))
        for i in self.initTagProb: self.initTagProb[i] =  self.initTagProb[i]/len(sentences)
        self.initTagProb = dict(sorted(self.initTagProb.items(), key=lambda x: x[1], reverse=True)) #sort in decreasing order.

        # Dict of all POS tags, with values being the Probability of the POS tagg folling it. 
        # prabibility = count/amount of tokens.
        POSTransitions = [(sentence[i][1], sentence[i+1][1]) for sentence in sentences for i in range(len(sentence)-1)]
        self.transProb = dict(Counter(POSTransitions))
        for i in self.transProb: self.transProb[i] =  self.transProb[i]/len(POSTransitions)
        self.transProb = dict(sorted(self.transProb.items(), key=lambda x: x[1], reverse=True)) #sort in decreasing order.
  
        # Dict of all token tags, with values being the Probability of the POS tagg folling it. 
        TokenTransitions = [(sentence[i][0].upper(), sentence[i][1]) for sentence in sentences for i in range(len(sentence))]
        self.emissionProb = dict(Counter(TokenTransitions))
        for i in self.emissionProb: self.emissionProb[i] =  self.emissionProb[i]/len(TokenTransitions)
        self.emissionProb = dict(sorted(self.emissionProb.items(), key=lambda x: x[1], reverse=True)) #sort in decreasing order.
        # smothing Laplace, add one to all the counts, so that they start at one.
        
        """
        for i in self.emissionProb: 
            print(i, '   \t = \t', self.emissionProb[i])
        for i in self.transProb: 
            print(i, '   \t = \t', self.transProb[i])
        for i in self.initTagProb: 
            print(i, '\t = \t', self.initTagProb[i])
        """

    def most_probable_tags(self, tokens):
        # For every token in the emission prob, return the hights POS tag. 
        keys  = [i for i in self.emissionProb.keys()]
        oupuwt = []
        for x in tokens:
            for i in keys: 
                if x.upper() ==  i[0]: 
                    oupuwt.append(i[1])
                    break
        
        return oupuwt

    def all_probable_tags(self, token):
        return [(x[1], self.emissionProb[x]) for x in self.emissionProb.keys() if (x[0] == token.upper())]

    def all_probable_POS(self, POS):
        return [[x[1], self.transProb[x]] for x in self.transProb.keys() if (x[0] == POS.upper())]

    def all_probable_next_POS(self, POSS, POS):
        POS_DICT = dict(POS)
        for i in POSS:
            #print(" old   :",  i[1])
            if i[0] in POS_DICT:
                i[1] *= POS_DICT[i[0]]
                #print(i[0], "\t  =", POS_DICT[i[0]]) 
            else:
                i[1] *= 1/self.lengthOfTags
                #print(i[0], "\t  =", 1/self.lengthOfTags) 
            #print(" new   :",  i[1])
        return POSS

    def greatest_POS(self, POSS):
        POS_DICT = dict(POSS)
        POS_DICT2 = dict(sorted(POS_DICT.items(), key=lambda x: x[1], reverse=True))
        return POS_DICT2

    def recursion():
        print(" FIRST WORD _________________\n")

        # Calculate the prevous tag's all NEXT POS
        list_1 = self.all_probable_tags(tokens[1])
        list_2 = self.all_probable_POS(self.most_probable_tags(tokens[1])[0])
        list_3 = self.all_probable_next_POS(list_2, list_1)
        print(" list_3 ",  list_3, "\n")

        # The current tags all POS
        list_4 = self.all_probable_tags(tokens[2])
        print(list_4, "\n")

        list_10 = self.all_probable_next_POS(list_3, list_4)
        print(list_10, "\n")

        print(self.greatest_POS(list_10), "\n")

        print(" SECCOND WORD _________________\n")

        # Calculate the prevous tag's all NEXT POS
        list_1 = self.all_probable_tags(tokens[1])
        list_2 = self.all_probable_POS(self.most_probable_tags(tokens[1])[0])
        list_3 = self.all_probable_next_POS(list_2, list_1)
        print(" list_3 ",  list_3, "\n")

        # The current tags all POS
        list_4 = self.all_probable_tags(tokens[2])
        print(list_4, "\n")

        list_5 = self.all_probable_next_POS(list_3, list_4)
        print(list_5, "\n")

        list_11 = self.all_probable_next_POS(list_5, list_10)
        print(list_11, "\n")

        print(self.greatest_POS(list_11), "\n")


    def viterbi_tags(self, tokens):
    	# copy week 9, meeting 27. page 13, sudo code.
        POSlist = set([i[0] for i in self.transProb.keys()])
        #print(POSlist)

        # Create a path probability matrix viterbi [N, T]
        # dict token with each POS
        dict_1 = {i:{j:0 for j in range(len(tokens))} for i in POSlist}
        dict_2 = {i:{j:0 for j in range(len(tokens))} for i in POSlist}


        # For each state s from 1 to N do 
        for pos in POSlist:
            #print("pos", pos)
            if (tokens[0].upper(),pos) in self.emissionProb:
                dict_1[pos][0] = log(self.initTagProb[pos]) + log(self.emissionProb[(tokens[0].upper(),pos)])
                #print("initTagProb", self.initTagProb[pos], "initTagProb log space", log(self.initTagProb[pos]))
                #print("emissionProb", self.emissionProb[(tokens[0],pos)], "emissionProb log space", log(self.emissionProb[(tokens[0],pos)]))
            else: 
                dict_1[pos][0] = log(self.initTagProb[pos]) + log(1/(self.lengthOfTags))
                #print("initTagProb", self.initTagProb[pos], "initTagProb log space", log(self.initTagProb[pos]))
                #print("lengthOfTags", 1/self.lengthOfTags, "lengthOfTags", log(1/(self.lengthOfTags)) )


        for i in range(1, len(tokens)):
            for pos in POSlist:
                #BROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
                


                # Get the max,!
                maxumum = float("-inf")
                maxPOS = None
                #
                for prevousPOS in POSlist:
                    
                    if (tokens[i].upper(),pos) in self.emissionProb:

                        current = dict_1[prevousPOS][i - 1] + log(self.transProb[(prevousPOS,pos)]) + log(self.emissionProb[(tokens[i].upper(),pos)])
                        #print("FOUND")
                    else: 
                        current = dict_1[prevousPOS][i - 1] + log(self.transProb[(prevousPOS,pos)]) + log(1/(self.lengthOfTags))
                        #print("help")


                    if current > maxumum:
                        maxumum = current
                        maxPOS = prevousPOS

                dict_1[pos][i] = maxumum
                dict_2[pos][i] = maxPOS

                

                
        maxumum = float("-inf")
        maxPOS = None
        for pos in POSlist:
            if dict_1[pos][len(tokens) - 1] > maxumum: 
                maxumum = dict_1[pos][len(tokens) - 1]
                maxPOS = pos

        list_69 = [maxPOS]

        i = len(tokens)-1
        while dict_2[maxPOS][i] != 0: 
            maxPOS = dict_2[maxPOS][i]
            list_69.append(maxPOS)
            i -= 1

        list_69.reverse()

        #print(dict_1)


        return list_69




############################################################
# Test Code
############################################################

"""
# 1
c = load_corpus("brown_corpus.txt")
print(c[1402])
c = load_corpus("brown_corpus.txt")
print(c[1799])

# 3
c = load_corpus("brown_corpus.txt")
t = Tagger(c)
print(t.most_probable_tags(["The", "man", "walks", "."]))
c = load_corpus("brown_corpus.txt")
t = Tagger(c)
print(t.most_probable_tags(["The", "blue", "bird", "sings"]))


# 4
c = load_corpus("brown_corpus.txt")
t = Tagger(c)
s = "I am waiting to reply".split()
print(t.most_probable_tags(s))
print(t.viterbi_tags(s))

c = load_corpus("brown_corpus.txt")
t = Tagger(c)
s = "I saw the play".split()
print(t.most_probable_tags(s))
print(t.viterbi_tags(s))
"""

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
20 Hours
"""

feedback_question_2 = """
using the books psudo code for viterbi_tags was not fun.
"""

feedback_question_3 = """
None; everything.
"""

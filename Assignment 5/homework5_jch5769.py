############################################################
# CMPSC442: Homework 5
############################################################

student_name = "John_Hofbauer"

############################################################
# Imports
# What modules can I import?  -- collections, itertools, math, random, queue, email, os, re, string, copy, os
############################################################

# Include your imports here, if any are used.
import os
from email import message_from_file, iterators
from math import log, exp
from collections import Counter, OrderedDict

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):

	# Open the file 
	file = open(email_path, "r", encoding="utf-8")
	# Create the list of tokens
	message = message_from_file(file)
	tokens = [token for lines in iterators.body_line_iterator(message) for token in lines.split()]
	# Close the file 
	# Return a list of the tokens from the file. 
	file.close(); return tokens

def log_probs(email_paths, smoothing):    
	# Create a list of the tokens 
    tokens = [token for email in email_paths for token in load_tokens(email)]
    tokenCountWithRepeats = len(tokens)
    # Create a dict for the count of each token.
    tokenCount = Counter(tokens)
    tokenCountWithoutRepeats = len(tokenCount)+1
    # create the probability dict, then apply smothing.
    # CMPSC 442, Wk 8, Mtg 22, Seg 2. FROM SLIDE 20 Mitigation: calculate in log space. Given log(xy) = log(x) + log(y)
    # 	preform all computaions by summing log of probabilites rather than multiplying prvabilits. 
    tokenProbabilitys = {token:(log((amount+smoothing)/((tokenCountWithRepeats)+(smoothing*(tokenCountWithoutRepeats))))) for token, amount in tokenCount.items()}
    tokenProbabilitys["<UNK>"] = log(smoothing/(tokenCountWithRepeats+(smoothing*(tokenCountWithoutRepeats))))
    # Return the dict of prbabilites.
    return tokenProbabilitys


class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
    	# Get a list of all the files within the dirctory. keeping the dictinary comprehention sepreate, increasses runtime. 
        spamFiles = [(spam_dir+'/'+i) for i in os.listdir(spam_dir)]
        hamFiles = [(ham_dir+'/'+i) for i in os.listdir(ham_dir)]
        spamFileAmount = len(spamFiles)
        hamFileAmount = len(hamFiles)

        # Create the dict for the index of all spam and ham emails. 
        self.Pspam = log_probs(spamFiles, smoothing)
        self.Pham = log_probs(hamFiles, smoothing) 

        # Calculate the probabilities.
        self.spamLogProbability = spamFileAmount / (spamFileAmount + hamFileAmount)
        self.hamLogProbability = hamFileAmount / (spamFileAmount + hamFileAmount)
    
    def is_spam(self, email_path):
        # Create a dict for the count of each token.
        tokenCount = Counter([token for token in load_tokens(email_path)])
        
        # Calculate the projuct of each token from the email, found within the data set.
        spamProduct = sum([self.Pspam[token] if token in self.Pspam else self.Pspam["<UNK>"] for token, count in tokenCount.items()])
        hamProduct = sum([self.Pham[token] if token in self.Pham else self.Pham["<UNK>"] for token, count in tokenCount.items()])

        # return a Boolen stating weather it is more probable that the email is spam or ham.
        return log(self.spamLogProbability)+spamProduct > log(self.hamLogProbability)+hamProduct
        
    def most_indicative_spam(self, n):
        # Calculate the token probabilites using log (P(w|spam)/P(w))
        tokenProbabilitys = {token:count-log((exp(self.Pham[token])+exp(self.Pspam[token]))) for token, count in self.Pham.items() if (token in self.Pspam)}
        #print('table 1', [i for i in tokenProbabilitys.items()][:10])

        # Return the list of keys, sorted by their values, then trunkated to only return the first n amount
        return [token[0] for token in sorted(tokenProbabilitys.items(), key=lambda x: x[1])][:n]

    def most_indicative_ham(self, n):
        # Calculate the token probabilites using log (P(w|spam)/P(w))
        tokenProbabilitys = {token:count-log((exp(self.Pspam[token])+exp(self.Pham[token]))) for token, count in self.Pspam.items() if (token in self.Pham)}

        # Return the list of keys, sorted by their values, then trunkated to only return the first n amount
        return [token[0] for token in sorted(tokenProbabilitys.items(), key=lambda x: x[1])][:n]


############################################################
# Test Code
############################################################

"""
import time
startTime = time.time()

# 1
ham_dir="homework5_data/train/ham/"
print(load_tokens(ham_dir+"ham1")[200:204])
print(load_tokens(ham_dir+"ham2")[110:114])
spam_dir="homework5_data/train/spam/"
print(load_tokens(spam_dir+"spam1")[1:5])
print(load_tokens(spam_dir+"spam2")[:4])

# 2
paths=["homework5_data/train/ham/ham%d"%i for i in range(1,11)]
p=log_probs(paths,1e-5)
print(p["the"])
print(p["line"])

paths=["homework5_data/train/spam/spam%d"%i for i in range(1,11)]
p=log_probs(paths,1e-5)
print(p["Credit"])
print(p["<UNK>"])

# 3

# 4
sf=SpamFilter("homework5_data/train/spam","homework5_data/train/ham",1e-5)
print(sf.is_spam("homework5_data/train/spam/spam1"))
print(sf.is_spam("homework5_data/train/spam/spam2" ))
sf = SpamFilter("homework5_data/train/spam", "homework5_data/train/ham", 1e-5)
print(sf.is_spam("homework5_data/train/ham/ham1"))
print(sf.is_spam("homework5_data/train/ham/ham2"))

# 5
sf=SpamFilter("homework5_data/train/spam", "homework5_data/train/ham",1e-5)
print(sf.most_indicative_spam(5))
sf=SpamFilter("homework5_data/train/spam", "homework5_data/train/ham",1e-5)
print(sf.most_indicative_ham(5))

print(time.time() - startTime)
"""

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
20 Hours - coding the assinment was eaiser that understanding why the
result was what it should be. 
"""

feedback_question_2 = """
Understanding the effects of smothing. (I know we went through it in class
but actualy using it, is diffrent.)
"""

feedback_question_3 = """
Ehh, it was better than the last assigment. 
I would have started with this assignment, since the order of the hw assignment 
has no real connection in my opinion.
"""

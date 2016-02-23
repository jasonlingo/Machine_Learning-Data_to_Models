#!/usr/bin/python

# ML: Data to Model homework1-b

import sys
import copy

''' This program computes conditional probability distributions of a given graph. 
	The graph is represented by a network_file which contains the nodes and edges, 
	and a cpd_file which contains all the cpd parameters. 
	
	Usage: 
	python cpd.py network_file cpd_file lefthand_side [righthand_side]
'''

##################################################
## Global variables
##################################################
graph = {} # a dictionary for all nodes
	
##################################################
## Class for node in the graph
##################################################
class Node:
	def __init__(self, name, values):
		self.name = name # string
		self.values = values #list of strings
		self.parents = [] # list of parents
		
		# conditional probability table:
		# keys are tuples of node values, values are probabilities
		# the key tuple elements are ordered the same as parents
		self.cpt = {} 
		
	def __str__(self):
		return self.name+" "+str(self.values)
	def set_parents(self, parents):
		self.parents=parents
	def add_cp(self, values, prob):
		self.cpt[values]=prob 
	def get_parents(self):
		return self.parents
	def get_cp(self, values):
		return self.cpt[values]
	def get_cpt(self):
		return self.cpt
	def get_values(self):
		return self.values
	
##################################################
## Function for calculating the total joint probability:
## The argument is a dictionary of the name-value pairs
## of all the nodes
##################################################
def total_joint(pairs):
	prob = 1.0
	for n in pairs:		
		# make a tuple of values
		parents = graph[n].get_parents()
		l = [pairs[n]]
		for p in parents:
			l.append(pairs[p])
		t = tuple(l)
		# get the cp from the node object
		prob *= graph[n].get_cp(t)
	return prob

##################################################
## Function for calculating the partial joint probability:
## The argument is a dictionary of name-value pairs that 
## are in the joint probability
##################################################
def partial_joint(pairs):

	# Algorithm:
	# Sum total joint probabilities over all possible values of
	# the nodes that are not in the pairs.
	# To iterate over all values of undetermined number of nodes, 
	# we need a list for node names, and a 2d list for all the value
	# permutations. 

	nodes = [] #list of strings
	value_lists = [] 
	value_lists.append([]) # a 2D list

	for n in graph:
		if (n not in pairs):
			nodes.append(n)
			augmented_list = []
			for v in graph[n].get_values():
				# for each value of n, get a full copy of value_lists
				# and append this value to the end of all value lists,
				# then combine these copies together as the new value_lists
				temp_list = copy.deepcopy(value_lists)
				for l in temp_list:
					l.append(v)
				augmented_list += temp_list
			value_lists = augmented_list 
	 
	# Now use the value_lists to iterate over the node values
	prob_sum = 0
	for values in value_lists:
		for i in range(len(values)): # make a pair list for total joint prob
			pairs[nodes[i]]=values[i]
		prob_sum += total_joint(pairs)
	
	return prob_sum


##################################################
## Read in graph files
##################################################
if len(sys.argv)<4:
	print "Need more arguments! \nUsage: "
	print "python cpd.py network_file cpd_file lefthand_side [righthand_side]"
	sys.exit() 
else:
	network_file = sys.argv[1]
	cpd_file = sys.argv[2]

# read the network file and build the node and graph objects
# we don't need to read the edges since the cpd file tells everything
network = open(network_file)
node_num = int(network.readline())

for i in range(node_num):
	line = network.readline().split()
	name = line[0]
	values = line[1].split(",")
	node = Node(name, values)
	graph[name] = node
	
network.close()

# read the cpd file and build cpt(conditional probability table)
cpd = open(cpd_file)

for line in cpd:
	parents = []
	values = []
	ls = line.split()
	if not ls:
		continue
	lhs = ls[0].split("=") # the LHS of the cpd: name and value
	node = graph[lhs[0]] # get the node with the name
	values.append(lhs[1]) # the first value is the lhs value
	rhs = ls[1].split(",")  # get the names and values of parents
	
	for e in rhs:
		p = e.split("=")
		parents.append(p[0])
		values.append(p[1])
	
	if len(node.get_parents())==0: # if it's the first time to set the node
		node.set_parents(parents)
	
	node.add_cp(tuple(values),float(ls[2]))

cpd.close

# find the root nodes and assign uniform distribution if probabilities not given
for n in graph:
	if len(graph[n].get_cpt())==0:
		values = graph[n].get_values()
		for v in values:
			t = (v,) # make a tuple for the value
			p = 1.0/len(values)
			graph[n].add_cp(t,p)

# for n in graph:
# 	print graph[n].get_cpt()
			
##################################################
## Compute CPD
##################################################

# build the query hashes from command line 
event = {}
condition = {}

lhs = sys.argv[3]
lhs_list = lhs.split(",")
for e in lhs_list:
	p = e.split("=")
	if p[0] not in graph:
		sys.exit("Invalid node name \""+p[0]+"\" in LHS!")
	if p[1] not in graph[p[0]].get_values():
		sys.exit("Invalid value \""+p[1]+"\" in LHS!")
	event[p[0]]=p[1]

if len(sys.argv)==5:
	rhs = sys.argv[4]
	rhs_list = rhs.split(",")	
	for e in rhs_list:
		p = e.split("=")
		if p[0] not in graph:
			sys.exit("Invalid node name \""+p[0]+"\" in RHS!")
		if p[1] not in graph[p[0]].get_values():
			sys.exit("Invalid value \""+p[1]+"\" in RHS!")
		condition[p[0]]=p[1]
	
# Use Bayes Theory to calculate the conditional probability 

# The joint probability in the numerator:
pairs = copy.copy(event)
pairs.update(condition)
prob = partial_joint(pairs)

# Divide it by the joint probability in the denominator (if condition given) 
if condition:
	deno = partial_joint(condition)
	prob /= deno

print "The conditional probability is: "
print '%.13e' % (prob)




























		
#!/usr/bin/env python3
import queue
# https://www.geeksforgeeks.org/python-program-to-sort-a-list-of-tuples-by-second-item/
# https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1


def slowComplete(prefix, list_of_words, top):
	"""
	For a given prefix, provide top suggestions from this list of words.

	Parameters
	----------
	prefix: Signal word used here
	list_of_words: a file that has the example format
	top: top many suggestions as output

	Return
	------
	the top k recommendations with given prefix and list


	"""
	file = open(list_of_words, 'r')
	data = file.readlines()
	data_list = []
	for i in range(len(data)):
		if i != 0:
			data_list.append(data[i])
	num_list = []
	word_list = []
	for l in data_list:
		if l != '\n':
			entry = l.split('\t')
			num_list.append(int(entry[0]))
			word_list.append(entry[1][:-1])
	candidate_list = []
	for i in range(len(word_list)):
		if word_list[i].startswith(prefix):
			candidate_list.append((word_list[i],num_list[i]))
	sorted(candidate_list, key=lambda x: x[1])
	final_list = candidate_list[0:top]
	return(final_list)


###################
## Make Trie ##
###################




class TrieNode:

	
	def __init__(self, char=None, weight=None, isEnd = False, max_weight = 0):
		self.char = char
		self.weight = weight
		self.children = {}
		self.isEnd = isEnd
		# self.max_weight = max_weight



		
class Trie:

	def __init__(self):
		self.root = TrieNode()

	def insert(self, word, weight):
		node = self.root
		for i in range(len(word)):
			char = word[i]
			found_in_children = False
			if char in node.children:
				node.children[char].weight = max(weight, node.children[char].weight)
				node = node.children[char]
				found_in_children = True
				if i == len(word) - 1:#if this word matches at evert step, create a virtual node to indicate its values, so I don't need both weight and max_weight
						node.children[''] = (TrieNode(char = '', weight = weight))
						node = node.children['']
						node.isEnd = True
			if found_in_children == False:
				new_node = TrieNode(char, weight)
				node.children[new_node.char] = new_node
				node = new_node
		node.isEnd = True

	# 	for child in node.children.keys():
	# 		if child == char and node.children[child].isEnd != True:
	# 			node.children[child].max_weight =  max(weight, node.children[child].max_weight)
	# 			node = node.children[child]
	# 			found_in_children = True
	# 			if i == len(word) - 1:
	# 				node.children[''] = (TrieNode(char = '', weight = weight))
	# 				node.children[''].max_weight = weight
	# 				node = node.children['']
	# 				node.isEnd = True
	# 	if found_in_children == False:
	# 		new_node = TrieNode(char, weight)
	# 		new_node.max_weight = new_node.weight
	# 		node.children[new_node.char] = new_node
	# 		node = new_node
	# node.isEnd = True
		


	def search(self,prefix):
		node = self.root
		for char in prefix:
			char_not_found = True
			for child in node.children.keys():
				if child == char:
					char_not_found = False
					node = node.children[child]
					break
			if char_not_found:
				return 0
		return node



def read_file(filepath):
	"""
	for a given file, change it into list of words and numbers, will call this in build_trie

	Parameters
	----------
	filepath: Name of the file we will use

	Return
	------
	a list of words and a list of corresponding weights


	"""
	file = open(filepath, 'r',encoding = "utf-8")
	data = file.readlines()
	data_list = []
	for i in range(len(data)):
		if i != 0:
			data_list.append(data[i])
	num_list = []
	word_list = []
	for l in data_list:
		if l != '\n':
			entry = l.split('\t')
			num_list.append(int(entry[0]))
			word_list.append(entry[1][:-1])
	return num_list,word_list


def build_trie(text):
	"""
	read in a file, transform it into our desired form, and build a trie for that text file

	Parameters
	----------
	text: a text file we will use

	Return
	------
	a trie that will have all the arrtibute and function above


	"""
	trie = Trie()
	numbers, words = read_file(text)
	for i in range(len(words)):
		trie.insert(words[i],numbers[i])
	return trie

# Use the python file priority queue from 750 git

class PriorityQueue:
    def __init__(self):
        self.q = queue.PriorityQueue()

    def is_empty(self):
        return self.q.empty()

    def extract_highest(self):
        priority, item = self.q.get_nowait()
        return item

    def insert(self, item, priority):
        self.q.put_nowait((-priority, item))
		




def add(trie, word, weight):
	"""
	add one more term to the trie with new word and weight

	Parameters
	----------
	word:as described above
	weight:as described above

	Return
	------
	a new trie with the new word inserted


	"""
	trie.insert(word,weight)#we can do this since in my insert function it helps me update weight
	return trie


def change_weight(trie, word,function):
	"""
	change the weight of a target word

	Parameters
	----------
	word: the target word we want to change weight
	function: some function that I want to change the weight to be, can be an add 1 or rescaling

	Return
	------
	a new trie that has an original word with new weight


	"""
	weight = trie.search(word).weight
	new_weight = function(weight)
	if new_weight > weight:
		add(trie, word, new_weight)
	else:
		delete(trie, word)
		add(trie, word, new_weight)
	return trie

def delete(trie, word):
	"""
	search the trie and identify all nodes
	if at one node it contains child only from character of this word,delete everything below the node
	update the weight if at some level it is the maximum

	Parameters
	----------
	word: the target word we want to delete

	Return
	------
	a new trie that has the targeted word removed


	"""
	for i in range(len(word)):
		n = len(word)
		cur_word = word[:n-i]
		if trie.search(cur_word) != 0:
			cur_node = trie.search(cur_word)
			cur_parent = trie.search(cur_word[:len(cur_word)-1])
			if i == 0:
				if len(cur_node.children.keys()) >= 1:
					cur_node.isEnd == False
					cur_node_weight_list = []
					for child in cur_node.children.keys():
						cur_node_weight_list.append(cur_node.children[child].weight)
					if len(cur_node_weight_list) != 0:
						cur_node.weight = max(cur_node_weight_list)
				else:
					cur_parent.children.pop(cur_node.char)
					max_list = []
					for i in cur_parent.children.keys():
						max_list.append(cur_parent.children[i].weight)
					if max_list != []:
						cur_parent.weight = max(max_list)
			else:
				if cur_node.isEnd == False and len(cur_node.children.keys()) < 1:
					cur_parent.children.pop(cur_node.char)
					max_list = []
					for i in cur_parent.children.keys():
						max_list.append(cur_parent.children[i].weight)
					if max_list != []:
						cur_parent.weight = max(max_list)

			# if len(cur_node.children.keys()) < 1 and (i == 0 or (i > 0 and not cur_node.isEnd)):
			# 	cur_parent.children.pop(cur_node.char)
			# 	for i in cur_parent.children.keys():
			# 		max_list.append(cur_parent.children[i].weight)
			# 	if max_list != []:
			# 		cur_parent.weight = max(max_list)
			# else:
			# 	if i == 0:
			# 		cur_node.isEnd = False
			# 	for i in cur_parent.children.keys():
			# 		max_list.append(cur_parent.children[i].weight)
			# 	if max_list != []:
			# 		cur_parent.weight = max(max_list)
	return trie

def insert_or_update(trie,word,weight):
	"""
	check if a word is in the trie, if in, increase weight by 1, else insert the word

	Parameters
	----------
	word: the target word we want to update
	weight: the weight of the word

	Return
	------
	a new trie that has the targeted updated


	"""
	if trie.search(word) != 0:
		change_weight(trie,word,lambda x: x + 1)
	else:
		add(trie, word, weight)

def prune_trie(trie, threshold):
	"""
	search through the trie and delete words that have weight less than the threshold
	this is a grand level function that makes the trie with fewer nodes.

	Parameters
	----------
	threshold: the minimum weight we want to keep in the trie

	Return
	------
	a new trie that has been pruned


	"""
	node = trie.root
	pq = []
	for i in node.children.keys():
		pq.append((node.children[i],node.children[i].char))
	while len(pq) > 0:
		cur_node, char = pq.pop()
		if cur_node.isEnd == False:
			for i in cur_node.children.keys():
				pq.append((cur_node.children[i],char + cur_node.children[i].char))
		else:
			if cur_node.weight < threshold:
				delete(trie, char)
			else:
				continue
	return trie



def rescale_weights(trie, function):
	"""
	search through the trie and update the weight of the words
	this is a grand level function that makes the trie with different weights

	Parameters
	----------
	function: the change weight function we are going to use, like f(x) = x+1, f(x) = x/1000, f(x) = log(x)

	Return
	------
	a new trie that has been rescaled


	"""
	node = trie.root
	pq = []
	for i in node.children.keys():
		pq.append((node.children[i],node.children[i].char))
	while len(pq) > 0:
		cur_node, char = pq.pop()
		if cur_node.isEnd == False:
			for i in cur_node.children.keys():
				pq.append((cur_node.children[i],char + cur_node.children[i].char))
		else:
			change_weight(trie, char, function)
	return trie

			


def autoComplete(prefix, Trie, top):
	"""
	main function that give suggestions, search through the whole trie, push items into the priority queue and knit characters together 
	into full words

	Parameters
	----------
	prefix: The thing we want to begin with
	Trie: a pre-built trie using build_trie function
	top: number of suggestions

	Return
	------
	a list of words and corresponding weight


	"""
	temp_node = Trie.search(prefix)
	suggest_list = []
	word_list = []
	Pqueue = PriorityQueue()
	for child in temp_node.children.keys():
		node = temp_node.children[child]
		Pqueue.insert((child,node), node.weight)
	for i in range(top):
		word_list.append(prefix)
	while len(suggest_list) < top and Pqueue.is_empty() == False:
		character, candidate_node = Pqueue.extract_highest()
		if candidate_node.isEnd == False:
			for child in candidate_node.children.keys():
				Pqueue.insert((character+child,candidate_node.children[child]), candidate_node.children[child].weight)
		else:
			word_list[len(suggest_list)] = word_list[len(suggest_list)] + character
			suggest_list.append((word_list[len(suggest_list)], candidate_node.weight))
	return suggest_list





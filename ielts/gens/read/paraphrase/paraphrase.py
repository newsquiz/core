from PyDictionary import PyDictionary
from enlp import POS
from enlp import DependencyParser
from .synonym_paraphrase import synonym_paraphrase
from .active_passive import active_passive_paraphrase


def dfs(i, result, status, relations):
	if (i >= len(relations)):
		status_ = [i for i in status]
		result.append(status_)
		return result

	for x in relations[i]:
		status.append(x)
		result = dfs(i + 1, result, status, relations)
		status.remove(x)

	return result


def get_pos_conll(text, pos):
	words = ['']
	xpos = ['']
	raw_pos = pos.transform(text)
	print('rawpos = ', raw_pos)
	for pos in raw_pos[0]:
		words.append(pos.word)
		xpos.append(pos.pos_tag)
	return words, xpos


def get_dp_conll(text, words, xpos, dependparser):
	raw_dp = dependparser.predict({'text' : text})
	# declare list of dependency trees
	dependency_trees = []

	# make a tuple of relations
	relations = []

	for dependency in raw_dp['dependparser'][0]:
		head = dependency.root_index + 1
		tail = dependency.target_index + 1
		label = dependency.label
		if (label == 'nsubj:xsubj'):
			continue
		is_exist = False
		for i in range(len(relations)):
			for j in range(len(relations[i])):
				if ((relations[i][j][0] == head) and (relations[i][j][1] == tail)) or ((relations[i][j][0] == tail) and (relations[i][j][1] == head)):
					is_exist = True
					relations[i].append([head, tail, label])
					break
			if is_exist:
				break
		if not is_exist:
			relations.append([[head, tail, label]])

	# devide all relation in to corespnding no-loop trees
	dependency_relations = dfs(0, [], [], relations)

	# generate dependency trees
	for dependency_relation in dependency_relations:
		# declare lists
		labels = ['']
		heads = [-1]
		for i in range(1, len(words)):
			labels.append('root')
			heads.append(0)
		# generate tree
		for relation in dependency_relation:
			heads[relation[1]] = relation[0]
			labels[relation[1]] = relation[2]
		dependency_trees.append({'words' : words, 'xpos' : xpos, 'heads' : heads, 'labels': labels})

	return dependency_trees


def get_paraphrases(text, pos, dependparser, verb_dictionary):
	### declare paraphrases
	paraphrases = {'text' : text, 'sentence_paraphrases' : []}
	### get dependency trees
	words, xpos = get_pos_conll(text, pos)
	dependency_trees = get_dp_conll(text, words, xpos, dependparser)
	paraphrases['sentence_paraphrases'].append(' '.join(words))
	### synonym paraphase
	paraphrases['word_paraphrases'] = synonym_paraphrase(words, xpos)
	### active passive paraphrase
	for dependency_tree in dependency_trees:
		words = dependency_tree['words']
		xpos = dependency_tree['xpos']
		heads = dependency_tree['heads']
		labels = dependency_tree['labels']
		paraphased = active_passive_paraphrase(words, xpos, heads, labels, verb_dictionary)
		if (paraphased != words):
			paraphrases['sentence_paraphrases'].append(' '.join(paraphased))
	return paraphrases


class Paraphrase(object):
	def __init__(self, pos, dependparser):
		self.pos = pos
		self.dependparser = dependparser
		self.load_verb_data()


	def load_verb_data(self):
		self.verb_dictionary = {}
		self.verb_dictionary['verb_base_form'] = []
		self.verb_dictionary['verb_3rd_present'] = []
		self.verb_dictionary['verb_gerund'] = []
		self.verb_dictionary['verb_past_tense'] = []
		self.verb_dictionary['verb_past_participle'] = []
		f = open('./ielts/gens/read/paraphrase/verb.tsv', 'r')
		for row in f:
			row_split = row[:-1].split('\t')
			self.verb_dictionary['verb_base_form'].append(row_split[0])
			self.verb_dictionary['verb_3rd_present'].append(row_split[1])
			self.verb_dictionary['verb_gerund'].append(row_split[2])
			self.verb_dictionary['verb_past_tense'].append(row_split[3])
			self.verb_dictionary['verb_past_participle'].append(row_split[4])


	def fit(self):
		pass


	def transform(self, text):
		paraphrases = get_paraphrases(text, self.pos, self.dependparser, self.verb_dictionary)
		return paraphrases
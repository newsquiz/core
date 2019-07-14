import pdb
import random
import numpy as np 
from nltk.corpus import wordnet as wn 
from .generate_question_dp.generate_acl_question import generate_acl_question
from .generate_question_dp.generate_subj_question import generate_subj_question
from .generate_question_dp.generate_cop_question import generate_cop_question
from .generate_question_dp.generate_dobj_question import generate_dobj_question
from .generate_question_dp.generate_ccomp_question import generate_ccomp_question
from .generate_question_dp.generate_xcomp_question import generate_xcomp_question
from .generate_question_dp.generate_tmod_question import generate_tmod_question
from .generate_question_dp.generate_amod_question import generate_amod_question
from .generate_question_dp.generate_nmod_question import generate_nmod_question
from .generate_question_dp.generate_nummod_question2 import generate_nummod_question
"""
	done: nsubj, nsubjpass, cop, acl

	problem: Enhence Dependency does not have tree form, it probaly have loop in tree. So we
	have to generate all no-loop tree form from origin tree. after that, generate questions and
	answers from each no-loop tree 
"""
verb_dictionary = {}
f = open('./generator/paraphrase/verb.tsv', 'r')
for row in f:
	row_split = row[:-1].split('\t')
	verb_dictionary[row_split[0]] = []
	verb_dictionary[row_split[0]].append(row_split[1])
	verb_dictionary[row_split[0]].append(row_split[2])
	verb_dictionary[row_split[0]].append(row_split[3])
	verb_dictionary[row_split[0]].append(row_split[4])

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

def get_dp_conll(raw_dp, words, xpos, ners):
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
		dependency_trees.append({'words' : words, 'xpos' : xpos, 'heads' : heads, 'labels': labels, 'ners' : ners})

	return dependency_trees


def get_pos_conll(raw_pos):
	words = ['']
	xpos = ['']

	for pos in raw_pos[0]:
		words.append(pos.word)
		xpos.append(pos.pos_tag)

	return words, xpos


def get_ner_conll(raw_ner):
	ners = ['']
	for ner in raw_ner[0]:
		ners.append(ner.ner_tag)
	return ners


def generate_question_QA(text, dependparser, pos, ner, entities):
	sentence = text
	### generate question and answers
	res = []
	### get conll form
	raw_pos = pos.transform(sentence)
	if (len(raw_pos) == 0):
		return res
	raw_dp = dependparser.predict({'text' : sentence})
	raw_ner = ner.transform(sentence)
	words, xpos = get_pos_conll(raw_pos)
	ners = get_ner_conll(raw_ner)
	dependency_trees = get_dp_conll(raw_dp, words, xpos, ners)
	
	for dependency_tree in dependency_trees:
		words = dependency_tree['words']
		xpos = dependency_tree['xpos']
		heads = dependency_tree['heads']
		labels = dependency_tree['labels']
		ners = dependency_tree['ners']
		print(words)
		print(xpos)
		print(heads)
		print(labels)
		print(ners)
		### generate subject question
		print('generate subj question')
		questions, answers, relations =  generate_subj_question(words, xpos, heads, labels, ners)
		for question, answer, relation in zip(questions, answers, relations):
			rank = 1
			res.append({'question' : question, 'answer' : answer, 'relation': relation, 'rank' : rank})
		
		### generate question for 'cop' label
		print('generate cop question')
		questions, answers, relations =  generate_cop_question(words, xpos, heads, labels, ners)
		for question, answer, relation in zip(questions, answers, relations):
			rank = 0
			res.append({'question' : question, 'answer' : answer, 'relation': relation, 'rank' : rank})

		### generate question for 'acl'
		print('generate acl question')
		questions, answers, relations =  generate_acl_question(words, xpos, heads, labels, ners)
		for question, answer, relation in zip(questions, answers, relations):
			rank = 0
			res.append({'question' : question, 'answer' : answer, 'relation': relation, 'rank' : rank})

		### generate question for 'ccomp'
		print('generate ccomp question')
		questions, answers, relations =  generate_ccomp_question(words, xpos, heads, labels, ners)
		for question, answer, relation in zip(questions, answers, relations):
			rank = 0
			res.append({'question' : question, 'answer' : answer, 'relation': relation, 'rank' : rank})

		### generate question for 'dobj'
		print('generate dobj question')
		questions, answers, relations =  generate_dobj_question(words, xpos, heads, labels, ners)
		for question, answer, relation in zip(questions, answers, relations):
			rank = 1
			if (question.find('How much') != -1):
				rank += 2
			res.append({'question' : question, 'answer' : answer, 'relation': relation, 'rank' : rank})

		### generate question for 'xcomp'
		print('generate xcomp question')
		questions, answers, relations =  generate_xcomp_question(words, xpos, heads, labels, ners)
		for question, answer, relation in zip(questions, answers, relations):
			rank = 0
			res.append({'question' : question, 'answer' : answer, 'relation': relation, 'rank' : rank})

		### generate question for 'tmod'
		print('generate tmod question')
		questions, answers, relations =  generate_tmod_question(words, xpos, heads, labels, ners)
		for question, answer, relation in zip(questions, answers, relations):
			rank = 2
			res.append({'question' : question, 'answer' : answer, 'relation': relation, 'rank' : rank})

		### generate question for 'amod'
		print('generate amod question')
		questions, answers, relations =  generate_amod_question(words, xpos, heads, labels, ners)
		for question, answer, relation in zip(questions, answers, relations):
			rank = 0
			res.append({'question' : question, 'answer' : answer, 'relation': relation, 'rank' : rank})

		### generate question for 'nmod'
		print('generate nmod question')
		questions, answers, relations =  generate_nmod_question(words, xpos, heads, labels, ners)
		for question, answer, relation in zip(questions, answers, relations):
			rank = 2
			res.append({'question' : question, 'answer' : answer, 'relation': relation, 'rank' : rank})
			
		### generate question for 'nummod'
		print('generate nummod question')
		questions, answers, relations =  generate_nummod_question(words, xpos, heads, labels, ners)
		for question, answer, relation in zip(questions, answers, relations):
			rank = 4
			res.append({'question' : question, 'answer' : answer, 'relation': relation, 'rank' : rank})
		
	for res_ in res:
		for e in entities:
			if (res_['answer'].find(e) != -1):
				res_['rank'] += 2
	res.sort(key = lambda res: res['rank'])

	return res


def nounify(word, pos_tag):
    verb_synsets = wn.synsets(word, pos=pos_tag)
    # Word not found
    if not verb_synsets:
        return []

    # Get all verb lemmas of the word
    verb_lemmas = []
    for s in verb_synsets:
        for l in s.lemmas():
            if str(l).split('.')[1] == pos_tag:
                verb_lemmas.append(l)

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) \
                                    for l in    verb_lemmas]

    # filter only the nouns
    nouns = set()
    for drf in derivationally_related_forms:
        for sub_drf in drf[1]:
            if (str(sub_drf).split(".")[1] == "n"):
                nouns.add(sub_drf.name())
    res = set()
    for noun in nouns:
        if noun[0] == word[0]:
            res.add(noun)
    # return all the possibilities sorted by probability
    return list(res)

def adjify(word, pos_tag):
    verb_synsets = wn.synsets(word, pos=pos_tag)
    # Word not found
    if not verb_synsets:
        return []

    # Get all verb lemmas of the word
    verb_lemmas = []
    for s in verb_synsets:
        for l in s.lemmas():
            if str(l).split('.')[1] == pos_tag:
                verb_lemmas.append(l)

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) \
                                    for l in    verb_lemmas]
    # filter only the adjs
    adjs = set()
    for drf in derivationally_related_forms:
        for sub_drf in drf[1]:
            if (str(sub_drf).split(".")[1] == "a"):
                adjs.add(sub_drf.name())
    res = set()
    for adj in adjs:
        if adj[0] == word[0]:
            res.add(adj)
    # return all the possibilities sorted by probability
    return list(res)

def advify(word, pos_tag):
    verb_synsets = wn.synsets(word, pos=pos_tag)
    # Word not found
    if not verb_synsets:
        return []

    # Get all verb lemmas of the word
    verb_lemmas = []
    for s in verb_synsets:
        for l in s.lemmas():
            if str(l).split('.')[1] == pos_tag:
                verb_lemmas.append(l)

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) \
                                    for l in    verb_lemmas]
    # filter only the advs
    advs = set()
    for drf in derivationally_related_forms:
        for sub_drf in drf[1]:
            if (str(sub_drf).split(".")[1] == "r"):
                advs.add(sub_drf.name())
    res = set()
    for adv in advs:
        if adv[0] == word[0]:
            res.add(adv)
    # return all the possibilities sorted by probability
    return list(res)

def verbify(word, pos_tag):
    """ Transform a verb to the closest noun: die -> death """
    verb_synsets = wn.synsets(word, pos=pos_tag)
    # Word not found
    if not verb_synsets:
        return []

    # Get all verb lemmas of the word
    verb_lemmas = []
    for s in verb_synsets:
        for l in s.lemmas():
            if str(l).split('.')[1] == pos_tag:
                verb_lemmas.append(l)

    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) \
                                    for l in    verb_lemmas]
    # filter only the advs
    verbs = set()
    for drf in derivationally_related_forms:
        for sub_drf in drf[1]:
            if (str(sub_drf).split(".")[1] == "v"):
                verbs.add(sub_drf.name())
    res = set()
    for verb in verbs:
        if verb[0] == word[0]:
            res.add(verb)
    # return all the possibilities sorted by probability
    return list(res)

def get_synonyms(word, sentence, pos_tag):
	morphy = wn.morphy(word, pos_tag)
	### get all synonyms
	meaning = lesk(sentence, morphy, pos_tag)
	syns = meaning.lemma_names()
	print(syns)

def generate_question_4FF(sentences, dependparser, pos, ner):
	noun_candidates = []
	verb_candidates = []
	adj_candidates  = []
	print("generate candidate")
	for sentence in sentences:
		# get conll form
		raw_pos = pos.transform(sentence)
		if (len(raw_pos) == 0):
			return res
		raw_dp = dependparser.predict({'text' : sentence})
		raw_ner = ner.transform(sentence)
		words, xpos = get_pos_conll(raw_pos)
		# get best Noun
		best_idx = -1
		best_noun = ""
		for i, (word, xp) in enumerate(zip(words, xpos)):
			if (xp in ["NN", "NNS"]):
				if (wn.morphy(word, 'n') != None) and (len(wn.morphy(word, 'n')) > len(best_noun)):
					best_idx = i
					best_noun = wn.morphy(word, 'n')
				elif len(word) > len(best_noun):
					best_idx = i
					best_noun = word
		if len(best_noun) != 0:
			noun_candidates.append((best_noun, best_idx, words))
		# get best verb
		best_idx = -1
		best_verb = ""
		for i, (word, xp) in enumerate(zip(words, xpos)):
			if (xp in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']):
				if (wn.morphy(word, 'v') != None) and (len(wn.morphy(word, 'v')) > len(best_verb)) and (word in verb_dictionary.keys()):
					best_idx = i
					best_verb = wn.morphy(word, 'v')
				elif (len(word) > len(best_verb)) and (word in verb_dictionary.keys()):
					best_idx = i
					best_verb = word
		if len(best_verb) != 0:
			verb_candidates.append((best_verb, best_idx, words))
		# TODO: adv - R and RB
		# # get best adj
		# best_idx = -1
		# best_adj = ""
		# for i, (word, xp) in enumerate(zip(words, xpos)):
		# 	if (xp in adj_labels = ['JJ', 'JJR', 'JJS']) and (len(wn.morphy(word, 'a')) > best_adj):
		# 		best_idx = i
		# 		best_adj = wn.morphy(word, 'n')
		# if len(best_adj) != 0:
		# 	adj_candidates.append((best_adj, best_idx, words))
	# get best word in each tag and generate sentences
	print("generate answers set")
	# noun
	noun_res = None
	if len(noun_candidates) > 0:
		noun_candidates.sort(key = lambda x: -len(x[0]))
		noun_can = noun_candidates[0]
		answers = set()
		answers.add(noun_can[2][noun_can[1]])
		answers.add(noun_can[0])
		can_sets = list(set(adjify(noun_can[0], 'n') + advify(noun_can[0], 'n') + verbify(noun_can[0], 'n')))
		random.shuffle(can_sets)
		answers = list(answers) + can_sets
		if len(answers[:4]) >= 2:
			noun_res = (" ".join(noun_can[2][:noun_can[1]] + ["_____"] + noun_can[2][noun_can[1]+1:]), words[noun_can[1]], answers[:4])
	# verb
	verb_res = None
	if len(verb_candidates) > 0:
		verb_candidates.sort(key = lambda x: -len(x[0]))
		verb_can = verb_candidates[0]
		answers = set()
		answers.add(verb_can[2][verb_can[1]])
		answers.add(verb_can[0])
		can_sets = list(set(verb_dictionary[verb_can[0]]))
		random.shuffle(can_sets)
		answers = list(answers) + can_sets
		if len(answers[:4]) >= 2:
			verb_res = (" ".join(verb_can[2][:verb_can[1]] + ["_____"] + verb_can[2][verb_can[1]+1:]), words[verb_can[1]], answers[:4])

	return (noun_res, verb_res)


def generate_question_FF(sentences, dependparser, pos, ner):
	noun_candidates = []
	verb_candidates = []
	adj_candidates = []
	adv_candidates = []
	print("generate candidate")
	for sentence in sentences:
		# get conll form
		raw_pos = pos.transform(sentence)
		if (len(raw_pos) == 0):
			return res
		raw_dp = dependparser.predict({'text' : sentence})
		raw_ner = ner.transform(sentence)
		words, xpos = get_pos_conll(raw_pos)
		# get best Noun
		idxs = []
		for i, (word, xp) in enumerate(zip(words, xpos)):
			if (xp in ["NN", "NNS"]):
				idxs.append(i)
		if len(idxs) > 0:
			_id = random.choice(idxs)
			noun_candidates.append((" ".join(words[:_id] + ["_____"] + words[_id+1:]), words[_id]))
		# get best verb
		idxs = []
		for i, (word, xp) in enumerate(zip(words, xpos)):
			if (xp in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']):
				idxs.append(i)
		if len(idxs) > 0:
			_id = random.choice(idxs)
			verb_candidates.append((" ".join(words[:_id] + ["_____"] + words[_id+1:]), words[_id]))
		# get best adj
		idxs = []
		for i, (word, xp) in enumerate(zip(words, xpos)):
			if (xp in ['JJ', 'JJR', 'JJS']):
				idxs.append(i)
		if len(idxs) > 0:
			_id = random.choice(idxs)
			adj_candidates.append((" ".join(words[:_id] + ["_____"] + words[_id+1:]), words[_id]))
		# get best adv
		idxs = []
		for i, (word, xp) in enumerate(zip(words, xpos)):
			if (xp in ['RB', 'RBR', 'RBS']):
				idxs.append(i)
		if len(idxs) > 0:
			_id = random.choice(idxs)
			adv_candidates.append((" ".join(words[:_id] + ["_____"] + words[_id+1:]), words[_id]))
	# get best word in each tag and generate sentences
	print("generate answers set")
	# noun
	noun_res = None
	if len(noun_candidates) > 0:
		noun_res = random.choice(noun_candidates)
	verb_res = None
	if len(verb_candidates) > 0:
		noun_res = random.choice(verb_candidates)
	adj_res = None
	if len(adj_candidates) > 0:
		adj_res = random.choice(adj_candidates)
	adv_res = None
	if len(adv_candidates) > 0:
		adv_res = random.choice(adv_candidates)
	return (noun_res, verb_res, adj_res, adv_res)

	



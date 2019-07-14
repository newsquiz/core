import numpy as np 
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


def generate_question(text, dependparser, pos, ner, entities):
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

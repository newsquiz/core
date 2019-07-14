"""
	ccomp: clausal complement
	Verb -- ccomp -- Verb : 68%
	Verb -- ccomp -- Adj  : 10%
	Verb -- ccomp -- Noun : 9%
	Eg: He says that you like to swim
	=> question: what he say? = what + nsubj (subject of verb) + verb
	=> answer  : you like swim = clausal complement
"""

from .extended_function import check_belong_to, get_noun_info


def generate_ccomp_question(words, xpos, heads, labels, ners):
	###
	questions = []
	answers = []
	relations = []
	verb_labels = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
	adj_labels = ['JJ', 'JJR', 'JJS']
	noun_labels = ['NN', 'NNP', 'NNS', 'NNPS']
	nsubj_labels = ['nsubj', 'nsubjpass']

	### find all ccomp relations
	for i in range(1, len(labels)):
		if (labels[i] == 'ccomp'):
			head_id = heads[i]
			tail_id = i

			### VERB ----ccomp----> VERB/ADJ/NOUN
			if ((xpos[head_id] in verb_labels) and (xpos[tail_id] in (verb_labels + adj_labels + noun_labels))):
				### --Nsubject--> VERB --ccomp--> VERB
				# get nsubj of sentence
				nsubj = ''
				for j in range(1, len(labels)):
					if ((heads[j] == head_id) and (labels[j] in nsubj_labels)):
						nsubj = ''
						for k in range(1, len(labels)):
							if (check_belong_to(j, k, heads)):
								nsubj += ' ' + words[k]

				# can not generate question without subject
				if (nsubj == ''):
					continue
				nsubj = nsubj[1:]

				# get all clausal complement except 'mark' relation
				verb_clausal = ''
				illegal_id = []
				for j in range(1, len(labels)):
					if ((heads[j] == i) and (labels[j] in ['mark'])):
						for k in range(1, len(labels)):
							if (check_belong_to(j, k, heads)):
								illegal_id.append(k)

				for j in range(1, len(labels)):
					if ((j not in illegal_id) and (check_belong_to(i, j, heads))):
						verb_clausal += ' ' + words[j]
				verb_clausal = verb_clausal[1:]

				# generate question
				question = 'what ' + nsubj + ' ' + words[head_id]
				answer = verb_clausal

				# append
				questions.append(question + '?')
				answers.append(answer)
				relations.append('ccomp')
	### return
	return questions, answers, relations

"""
	xcomp: open clausal complement
	66% VERB -- xcomp -- VERB
	Eg: Sue asked George to respond to her offer
	question: what does Sue ask Google to do? = what + subject + verb + object + do?
	answer  : respond to her offer = clausal
"""

from .extended_function import check_belong_to, get_noun_info


def generate_xcomp_question(words, xpos, heads, labels, ners):
	questions = []
	answers = []
	relations = []
	verb_labels = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
	adj_labels = ['JJ', 'JJR', 'JJS']
	noun_labels = ['NN', 'NNP', 'NNS', 'NNPS']
	nsubj_labels = ['nsubj', 'nsubjpass']
	obj_labels = ['dobj', 'iobj', 'obj']
	### find xcomp realtion
	for i in range(1, len(labels)):
		if (labels[i] == 'xcomp'):
			head_id = heads[i]
			tail_id = i
			### =============     VERB -- xcomp --> VERB    ========================
			if ((xpos[i] in verb_labels) and (xpos[heads[i]] in verb_labels)):
				# get nsubj of sentence
				nsubj = ''
				nsubj_id = -1
				for j in range(1, len(labels)):
					if ((heads[j] == head_id) and (labels[j] in nsubj_labels)):
						nsubj = ''
						nsubj_id = j
						for k in range(1, len(labels)):
							if (check_belong_to(j, k, heads)):
								nsubj += ' ' + words[k]
				if (nsubj == ''):
					continue

				# get verb phrase (all words belong to verb)
				verb = ''
				for j in range(1, len(labels)):
					if ((heads[j] == head_id) and (labels[j] in ['aux', 'auxpass', 'xcomp', 'ccomp', 'neg']) and (j != tail_id)) or (j == head_id):
						verb += ' ' + words[j]
				verb = verb[1:]
				
				# get object of sentence
				obj = ''
				for j in range(1, len(labels)):
					if ((heads[j] == head_id) and (labels[j] in obj_labels)):
						obj = ''
						for k in range(1, len(labels)):
							if (check_belong_to(j, k, heads)):
								obj += ' ' + words[k]

				# get all clausal belong to tail verb except 'mark' relation and check whether mark-word is to
				verb_clausal = ''
				mark_word = ''
				illegal_id = []
				for j in range(1, len(labels)):
					if ((heads[j] == i) and (labels[j] in ['mark'])):
						if (words[j].lower() == 'to'):
							mark_word = 'to'
						for k in range(1, len(labels)):
							if (check_belong_to(j, k, heads)):
								illegal_id.append(k)

				for j in range(1, len(labels)):
					if ((j not in illegal_id) and (check_belong_to(i, j, heads))):
						verb_clausal += ' ' + words[j]
				verb_clausal = verb_clausal[1:]

				# get all word in the end of sentence point to head_id except words belong to tail_id
				illegal_id = []
				last_id = -1
				for j in range(1, len(labels)):
					if (check_belong_to(tail_id, j, heads)):
						illegal_id.append(j)
						last_id = j

				end_sen = ''
				for j in range(last_id + 1, len(labels)):
					if (check_belong_to(head_id, j, heads)):
						end_sen += ' ' + words[j]
				end_sen = end_sen[1:]

				# get noun info
				is_human, type_noun = get_noun_info(words[nsubj_id], xpos[nsubj_id])

				# generate question
				if (mark_word == 'to'):
					if (xpos[head_id] == 'VBP'):
						question = 'what do' + nsubj + ' ' + verb + ' ' + obj + ' to do' + ' ' + end_sen
					else:
						if (xpos[head_id] == 'VBZ'):
							question = 'what does' + nsubj + ' ' + verb + ' ' + obj + ' to do' + ' ' + end_sen
						else:
							question = 'what did' + nsubj + ' ' + verb + ' ' + obj + ' to do' + ' ' + end_sen
				else:
					if (xpos[head_id] == 'VBP'):
						question = 'what do' + nsubj + ' ' + verb + ' ' + obj + ' do' + ' ' + end_sen
					else:
						if (xpos[head_id] == 'VBP'):
							question = 'what does' + nsubj + ' ' + verb + ' ' + obj + ' do' + ' ' + end_sen
						else:
							question = 'what did' + nsubj + ' ' + verb + ' ' + obj + ' do' + ' ' + end_sen
				answer = verb_clausal
				# append
				questions.append(question + '?')
				answers.append(answer)
				relations.append('xcomp')

			### =============     VERB -- xcomp --> NOUN    ========================
			### pass

	return questions, answers, relations
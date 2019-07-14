"""
	dobj: direct object
	70%: VERB -- dobj -- NOUN
	Eg: She gave me a raise
	question: what she gave me? = what + clausal (all words belong to Verb except dobj part which will be answer)
	answer  : a raise = all words belong to NOUN

	error: 1 câu hoặc 1 mệnh đề có thể có nhiều dobj
"""

from .extended_function import check_belong_to, get_noun_info


def generate_dobj_question(words, xpos, heads, labels, ners):
	###
	questions = []
	answers = []
	relations = []
	verb_labels = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
	adj_labels = ['JJ', 'JJR', 'JJS']
	noun_labels = ['NN', 'NNP', 'NNS', 'NNPS', 'PRP']
	nsubj_labels = ['nsubj', 'nsubjpass']
	### find all dobj relations
	for i in range(1, len(labels)):
		if (labels[i] == 'dobj'):
			head_id = heads[i]
			tail_id = i
			### VERB ----dobj----> NOUN
			if ((xpos[head_id] in verb_labels) and (xpos[tail_id] in noun_labels)):
				# check if exist nsubj point to head
				nsubj_id = -1
				for j in range(1, len(labels)):
					if (check_belong_to(head_id, j, heads) and (labels[j] in nsubj_labels)):
						nsubj_id = j
						break
				if (nsubj_id == -1):
					continue

				# get dobj
				dobj = ''
				illegal_id = []
				for j in range(1, len(labels)):
					if (check_belong_to(i, j, heads)):
						dobj += ' ' + words[j]
						illegal_id.append(j)
				dobj = dobj[1:]

				# get dobj info
				is_human, type_noun = get_noun_info(words[tail_id], xpos[tail_id])
				if (ners[tail_id] == 'PERSON'):
					is_human = True
				for j in range(1, len(heads)):
					if (heads[j] == tail_id) and (labels[j] in ['conj']):
						noun_type = 1
						
				# get body of question: the whole part belong to head except dobj will be the 
				# get nsubject
				nsubj = ''
				for j in range(1, len(heads)):
					if (check_belong_to(nsubj_id, j, heads)):
						nsubj += ' ' + words[j]
				nsubj = nsubj[1:]

				# get aux
				aux_id = -1
				for j in range(1, len(heads)):
					if (check_belong_to(head_id, j, heads) and (labels[j] in ['aux', 'auxpass'])):
						aux_id = j
						break

				# get verb
				verb = ''
				for j in range(1, len(heads)):
					if (j == head_id) or ((heads[j] == head_id) and (j != aux_id) and (labels[j] in ['aux', 'auxpass', 'advmod', 'neg'])):
						verb += ' ' + words[j]
				verb = verb[1:]

				# get extension
				extension = ''
				for j in range(head_id, len(heads)):
					if ((heads[j] == head_id) and ((len(labels[j]) >= 4) and (labels[j][:4] == 'nmod'))):
						for k in range(head_id, len(heads)):
							if (check_belong_to(j, k, heads)):
								extension += ' ' + words[k]
				extension = extension[1:]

				# generate question
				if (is_human):
					if (aux_id != -1):
						question = 'who ' + words[aux_id] + ' ' + nsubj + ' ' + verb + ' ' + extension
					else:
						question = 'who ' + nsubj + ' ' + verb + ' ' + extension
					if (xpos[head_id] == 'VBZ'):
						question = 'who does ' + nsubj + ' ' + verb + ' ' + extension
					if (xpos[head_id] == 'VBP'):
						question = 'who do ' + nsubj + ' ' + verb + ' ' + extension
					if (xpos[head_id] == 'VBD') and (aux_id == -1):
						question = 'who did ' + nsubj + ' ' + verb + ' ' + extension
				else:
					if (ners[tail_id] == 'MONEY'):
						if (aux_id != -1):
							question = 'How much ' + words[aux_id] + ' ' + nsubj + ' ' + verb + ' ' + extension
						else:
							question = 'How much ' + nsubj + ' ' + verb + ' ' + extension
						if (xpos[head_id] == 'VBZ'):
							question = 'How much does ' + nsubj + ' ' + verb + ' ' + extension
						if (xpos[head_id] == 'VBP'):
							question = 'How much do ' + nsubj + ' ' + verb + ' ' + extension
						if (xpos[head_id] == 'VBD') and (aux_id == -1):
							question = 'How much did ' + nsubj + ' ' + verb + ' ' + extension
					else:
						if (aux_id != -1):
							question = 'what ' + words[aux_id] + ' ' + nsubj + ' ' + verb + ' ' + extension
						else:
							question = 'what ' + nsubj + ' ' + verb + ' ' + extension
						if (xpos[head_id] == 'VBZ'):
							question = 'what does ' + nsubj + ' ' + verb + ' ' + extension
						if (xpos[head_id] == 'VBP'):
							question = 'what do ' + nsubj + ' ' + verb + ' ' + extension
						if (xpos[head_id] == 'VBD') and (aux_id == -1):
							question = 'what did ' + nsubj + ' ' + verb + ' ' + extension
				answer = dobj
				# append
				questions.append(question + '?')
				answers.append(answer)
				relations.append('dobj')
	### return
	return questions, answers, relations
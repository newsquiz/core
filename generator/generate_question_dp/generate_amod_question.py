"""
	amod: adjactive modifier
	88% NOUN -- amod -- ADJ
	Eg: Sam eats red meat
	question: how is meat that Sam eat?
	answer  : red

"""

from .extended_function import check_belong_to, get_noun_info


def generate_amod_question(words, xpos, heads, labels, ners):
	questions = []
	answers = []
	relations = []
	verb_labels = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
	adj_labels = ['JJ', 'JJR', 'JJS']
	noun_labels = ['NN', 'NNP', 'NNS', 'NNPS']
	nsubj_labels = ['nsubj', 'nsubjpass']
	obj_labels = ['dobj', 'iobj', 'obj']

	### find amod relation
	for i in range(1, len(labels)):
		if (labels[i] in ['amod']):
			head_id = heads[i]
			tail_id = i

			### form: NOUN -- amod -- ADJ
			if ((xpos[head_id] in noun_labels) and (xpos[tail_id] in adj_labels)):
				### find adj phrase (all words belong to adj - tail word)
				adj_phrase = ''
				illegal_id = []
				for j in range(1, len(heads)):
					if (check_belong_to(tail_id, j, heads)):
						adj_phrase += ' ' + words[j]
						illegal_id.append(j)
				adj_phrase = adj_phrase[1:]

				### find noun phrase (all word belong to noun - head word except all words belong to adj)
				for j in range(1, len(heads)):
					if (heads[j] == head_id) and (labels[j] not in ['det', 'cc', 'cc:preconj', 'compound', 'conj']) and (labels[j].find('nmod') == -1):
						for k in range(1, len(heads)):
							if (check_belong_to(j, k, heads)):
								illegal_id.append(k)

				noun_phrase = ''
				for j in range(1, len(heads)):
					if ((j not in illegal_id) and (check_belong_to(head_id, j, heads))):
						noun_phrase += ' ' + words[j]
				noun_phrase = noun_phrase[1:]

				### get noun info
				is_human, type_noun = get_noun_info(words[head_id], xpos[head_id])
				if (ners[head_id] == 'PERSON'):
					is_human = True
				for j in range(1, len(heads)):
					if (heads[j] == head_id) and (labels[j] in ['conj']):
						noun_type = 1
						
				### find direct verb phrase of subject (noun phrase)
				verb_id = -1
				for j in range(1, len(heads)):
					if ((heads[j] == 0) and (heads[j] == head_id) and (xpos[j] in verb_labels)):
						verb_id = j
						break

				verb_phrase = ''
				for j in range(1, len(heads)):
					if (check_belong_to(verb_id, j, heads)):
						verb_phrase += ' ' + words[j]
				verb_phrase = verb_phrase[1:]

				### generate question
				if (type_noun == 0):
					question = 'how ' + 'is ' + noun_phrase
				else:
					question = 'how ' + 'are ' + noun_phrase
				if (verb_id != -1):
					question += ' that ' + verb_phrase
				answer = adj_phrase

				### append
				questions.append(question + '?')
				answers.append(answer)
				relations.append('amod')

	return questions, answers, relations


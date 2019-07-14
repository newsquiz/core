"""
	cop: copula
	50% ADJ -- cop -- VERB
	36% NOUN -- cop -- VERB

	Eg: The light is on
	question: how is the light? = how is + nsubject?
	answer  : on = all words belong to ADJ (on)

	Eg: Bill is from California
	question: where is Bill? = where is + nsuject ?
	answer  : California = all words belong to NOUN (California)

	Eg: Bill is a man
	question: what is Bill? = what is + nsuject ?
	answer  : a man = all words belong to NOUN (man)
"""

from .extended_function import check_belong_to, get_noun_info, get_all_word_belong_to


def generate_cop_question(words, xpos, heads, labels, ners):
	###
	questions = []
	answers = []
	relations = []
	### find all word with cop label
	for i in range(1, len(labels)):
		if (labels[i] == 'cop') and (xpos[i] == 'VBZ'):
			obj_id = heads[i]
			### find all relations point to object
			object_relations = set()
			for j in range(1, len(labels)):
				if (heads[j] == obj_id):
					object_relations.add(labels[j])
			object_relations = list(object_relations)

			### find nsubj point to object
			nsubj = ''
			last_nsubj_id = -1
			for j in range(1, len(heads)):
				if ((labels[j] in ['nsubj', 'nsubjpass']) and (heads[j] == obj_id)):
					nsubj, last_nsubj_id = get_all_word_belong_to(j, words, heads)

			### find object
			obj = ''
			for j in range(last_nsubj_id + 1, len(heads)):
				if (check_belong_to(heads[obj_id], j, heads) and (labels[j] not in ['cop'])):
					obj += words[j] + ' '
			obj = obj[:-1]

			### generate question and answer
			question = ''
			answer = ''
			if (xpos[obj_id] in ['JJ', 'JJR', 'JJS']):
				question += 'how ' + words[i] + nsubj
				answer += obj
			else:
				if (('case' in object_relations) or ('prep' in object_relations)):
					question += 'where ' + words[i] + ' ' + nsubj
					answer += obj
				else:
					is_human, type_noun = get_noun_info(words[obj_id], xpos[obj_id])
					if (ners[obj_id] == 'PERSON'):
						is_human = True
					for j in range(1, len(heads)):
						if (heads[j] == obj_id) and (labels[j] in ['conj']):
							noun_type = 1
					if (is_human):
						question += 'who ' + words[i] + nsubj
					else:
						question += 'what ' + words[i] + nsubj
					answer += obj

			# append
			questions.append(question + '?')
			answers.append(answer)
			relations.append('cop')

	return questions, answers, relations
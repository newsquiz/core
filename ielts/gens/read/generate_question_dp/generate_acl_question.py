"""
	acl: clausal modifier of noun
	91% NOUN -- acl -- VERB
	2%  NOUN -- acl -- ADJ
	1%  NOUN -- acl -- NOUN
	Eg: I admire the fact that you are honest
	question: what is the fact that i admire? = what is + modified Noun + that + ...
	answer  : you are honest = clausal
"""
from .extended_function import check_belong_to, get_noun_info


def generate_acl_question(words, xpos, heads, labels, ners):
	###
	questions = []
	answers = []
	relations = []
	### find all acl relations
	for i in range(1, len(labels)):
		if (labels[i] in ['acl']):
			### get index of modified Noun in list
			noun_id = heads[i]

			### get all words belong to modified Noun except 'nsubj', 'nsubjpass', 'cop'
			noun_all = ''
			illegal_id = []
			for j in range(1, len(labels)):
				if (heads[j] == noun_id) and (labels[j] in ['nsubj', 'nsubjpass', 'cop', 'case']):
					for k in range(1, len(labels)):
						if (check_belong_to(j, k, heads)):
							illegal_id.append(k)
			for j in range(1, i):
				if ((j not in illegal_id) and (check_belong_to(noun_id, j, heads))):
					noun_all += ' ' + words[j]
			noun_all = noun_all[1:]

			### check is human
			is_human, noun_type = get_noun_info(words[noun_id], xpos[noun_id])
			if (ners[noun_id] == 'PERSON'):
				is_human = True
			for j in range(1, len(heads)):
				if (heads[j] == noun_id) and (labels[j] in ['conj']):
					noun_type = 1
					
			###	2 kind of question for Verb modify a Noun and Noun, Adj modify a Noun
			if (xpos[i] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']):
				### a verb modify a noun
				# get all word belong to verb
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

				# generate question and answer
				if (is_human):
					if (noun_type == 0):
						question = 'who is' + ' ' + verb_clausal
					else:
						question = 'who are' + ' ' + verb_clausal
				else:
					if (noun_type == 0):
						question = 'what is' + ' ' + verb_clausal
					else:
						question = 'what are' + ' ' + verb_clausal
				answer = noun_all
			else:
				### a Noun, Adj modify a noun
				# get all words belong to modified word
				full_clausal = ''
				illegal_id = []
				for j in range(1, len(labels)):
					if ((heads[j] == i) and (labels[j] in ['mark'])):
						for k in range(1, len(labels)):
							if (check_belong_to(j, k, heads)):
								illegal_id.append(k)

				for j in range(1, len(labels)):
					if ((j not in illegal_id) and (check_belong_to(i, j, heads))):
						full_clausal += ' ' + words[j]
				full_clausal = full_clausal[1:]

				# get all extended words
				extended_all = ''
				illegal_id = []
				for j in range(1, len(labels)):
					if (check_belong_to(noun_id, j, heads)):
						illegal_id.append(j)

				for j in range(1, len(labels)):
					if ((j not in illegal_id) and (check_belong_to(heads[noun_id], j, heads))):
						extended_all += ' ' + words[j]
				extended_all = extended_all[1:]

				# generate question and answer
				if (is_human):
					if (noun_type == 0):
						question = 'who is ' + noun_all + ' that ' + extended_all
					else:
						question = 'who are ' + noun_all + ' that ' + extended_all
				else:
					if (noun_type == 0):
						question = 'what is ' + noun_all + ' that ' + extended_all
					else:
						question = 'what are ' + noun_all + ' that ' + extended_all
				answer = full_clausal

			### append
			questions.append(question)
			answers.append(answer)
			relations.append('acl')
	### return
	return questions, answers, relations

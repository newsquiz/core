from .extended_function import check_belong_to, get_noun_info


def generate_subj_question(words, xpos, heads, labels, ners):
	###
	questions = []
	answers = []
	relations = []
	isHuman = False
	
	# find all word with nsubj label
	nsubj_labels = ['nsubj', 'nsubjpass']
	for i in range(1, len(labels)):
		if (labels[i] in nsubj_labels):
			### short question and answer
			# get all words belong to subject
			illegal_id = []
			for j in range(1, len(heads)):
				if ((labels[j] in ['ref', 'case', 'punct', 'appos']) and (heads[j] == i)):
					for k in range(1, len(heads)):
						if (check_belong_to(j, k, heads)):
							illegal_id.append(k)

			answer = ''
			for j in range(1, len(heads)):
				if (check_belong_to(i, j, heads)):
					if (j not in illegal_id):
						answer += ' ' + words[j]
					last_answer_id = j
			answer = answer[1:]

			# check noun info
			is_human, noun_type = get_noun_info(words[i], xpos[i])
			if (ners[i] == 'PERSON'):
				is_human = True
			for j in range(1, len(heads)):
				if (heads[j] == i) and (labels[j] in ['conj']):
					noun_type = 1

			# get all words belong to predicate
			illegal_id = []
			for j in range(last_answer_id + 1, len(heads)):
				if (heads[j] == heads[i]) and not (labels[j] in ['dobj', 'aux', 'auxpass', 'cop', 'advmod', 'ref', 'compound', 'neg']) and not ((len(labels[j]) >= 4) and (labels[j][:4] == 'nmod')):
					for k in range(1, len(heads)):
						if check_belong_to(j, k, heads):
							illegal_id.append(k)

			question_body = ''
			for j in range(last_answer_id + 1, len(heads)):
				if (j not in illegal_id) and (check_belong_to(heads[i], j, heads)):
					if (words[j] == 'am'):
						question_body += ' is'
					else:
						question_body += ' ' + words[j]
			if (question_body == ''):
				continue
			if is_human:
				question = 'who' + question_body
			else:
				question = 'what' + question_body

			# append
			questions.append(question + '?')
			answers.append(answer)
			relations.append('subj')

			### long question and answer
			# get all words belong to subject
			illegal_id = []
			for j in range(1, len(heads)):
				if ((labels[j] in ['ref', 'case', 'punct', 'appos']) and (heads[j] == i)):
					for k in range(1, len(heads)):
						if (check_belong_to(j, k, heads)):
							illegal_id.append(k)

			answer = ''
			for j in range(1, len(heads)):
				if (check_belong_to(i, j, heads)):
					if (j not in illegal_id):
						answer += ' ' + words[j]
					last_answer_id = j
			answer = answer[1:]
			# check noun info
			is_human, noun_type = get_noun_info(words[i], xpos[i])
			
			# get all words belong to predicate
			question_body = ''
			for j in range(last_answer_id + 1, len(heads)):
				if check_belong_to(heads[i], j, heads):
					if (words[j] == 'am'):
						question_body += ' is'
					else:
						question_body += ' ' + words[j]
			if (question_body == ''):
				continue
			if is_human:
				question = 'who' + question_body
			else:
				question = 'what' + question_body
			# append
			questions.append(question + '?')
			answers.append(answer)
			relations.append('subj')
			
	return questions, answers, relations
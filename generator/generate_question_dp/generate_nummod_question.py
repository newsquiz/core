"""
	nummod : numeric modifier of a noun
	64% Noun  -- nummod -- Num
	17% PropN -- nummod -- Num
	10% Sym   -- nummod -- Num
"""

from .extended_function import check_belong_to, get_noun_info


def generate_nummod_question(words, xpos, heads, labels, ners):
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
		"""
		=========================================================================================
		==== process sentences have form: subject(CD --nummod-- noun) + verb + ...===============
		=========================================================================================
		"""
		if (labels[i] in nsubj_labels) and (xpos[heads[i]] in verb_labels):
			###=== get all words belong to subject ==============================================
			illegal_id = []
			for j in range(1, len(heads)):
				if ((labels[j] in ['ref', 'case', 'punct']) and (heads[j] == i)):
					for k in range(1, len(heads)):
						if (check_belong_to(j, k, heads)):
							illegal_id.append(k)

			for j in range(1, len(heads)):
				if (check_belong_to(i, j, heads) and (j not in illegal_id)):
					last_answer_id = j
			###=== get nummod id ================================================================
			nummod_id = -1
			for j in range(len(labels)):
				if (heads[j] == i) and (labels[j] == 'nummod'):
					nummod_id = j
					break
			if (nummod_id == -1):
				continue
			###=== get nummod ===================================================================
			nummod = ''
			for j in range(len(labels)):
				if check_belong_to(nummod_id, j, heads):
					nummod += ' ' + words[j]
			nummod = nummod[1:]
			###=== get word[i] and its compound =================================================
			noun = ''
			for j in range(1, len(heads)):
				if (j == i) or ((heads[j] == i) and (labels[j] == 'compound')):
					noun += ' ' + words[j]
			noun = noun[1:]
			###=== generate question ============================================================
			question_body = ''
			for j in range(last_answer_id + 1, len(heads)):
				if (j not in illegal_id) and (check_belong_to(heads[i], j, heads)):
					if (words[j] == 'am'):
						question_body += ' is'
					else:
						question_body += ' ' + words[j]
			if (question_body == ''):
				continue
			question = 'How many ' + noun + ' ' + question_body
			###=== append =======================================================================
			questions.append(question + '?')
			answers.append(nummod + ' ' + words[i])
			relations.append('nummod')

		"""
		=========================================================================================
		=== process sentences have form: subject + verb + direct_object(CD -- nummod -- noun) ===
		=========================================================================================
		"""
		if (labels[i] == 'dobj') and (xpos[heads[i]] in verb_labels):
			head_id = heads[i]
			tail_id = i
			###=== VERB ----dobj----> NOUN -----nummod----->CD =================================
			if ((xpos[head_id] in verb_labels) and (xpos[tail_id] in noun_labels)):
				###=== check if exist nsubj point to head ======================================
				nsubj_id = -1
				for j in range(1, len(labels)):
					if (check_belong_to(head_id, j, heads) and (labels[j] in nsubj_labels)):
						nsubj_id = j
						break
				if (nsubj_id == -1):
					continue
				###=== get nummod id ===========================================================
				nummod_id = -1
				for j in range(len(labels)):
					if (heads[j] == tail_id) and (labels[j] == 'nummod'):
						nummod_id = j
						break
				if (nummod_id == -1):
					continue
				###=== get dobj info ============================================================
				is_human, type_noun = get_noun_info(words[tail_id], xpos[tail_id])
				if (ners[tail_id] == 'PERSON'):
					is_human = True
				for j in range(1, len(heads)):
					if (heads[j] == tail_id) and (labels[j] in ['conj']):
						noun_type = 1		
				###=== get body of question: the whole part belong to head except dobj ========== 
				###=== get nsubject =============================================================
				nsubj = ''
				for j in range(1, len(heads)):
					if (check_belong_to(nsubj_id, j, heads)):
						nsubj += ' ' + words[j]
				nsubj = nsubj[1:]
				###=== get word[i] and its compound =============================================
				noun = ''
				for j in range(1, len(heads)):
					if (j == i) or ((heads[j] == i) and (labels[j] == 'compound')):
						noun += ' ' + words[j]
				noun = noun[1:]
				###=== get nummod ===============================================================
				nummod = ''
				for j in range(len(heads)):
					if (check_belong_to(nummod_id, j, heads)):
						nummod += ' ' + words[j]
				nummod = nummod[1:]
				###=== get aux ==================================================================
				aux_id = -1
				for j in range(1, len(heads)):
					if (check_belong_to(head_id, j, heads) and (labels[j] in ['aux', 'auxpass'])):
						aux_id = j
						break
				###=== get verb =================================================================
				verb = ''
				for j in range(1, len(heads)):
					if (j == head_id) or ((heads[j] == head_id) and (j != aux_id) and (labels[j] in ['aux', 'auxpass'])):
						verb += ' ' + words[j]
				verb = verb[1:]
				###=== get extension ============================================================
				extension = ''
				for j in range(head_id, len(heads)):
					if ((heads[j] == head_id) and (((len(labels[j]) >= 4) and (labels[j][:4] == 'nmod')) or ((len(labels[j]) >= 5) and (labels[j][:5] == 'advcl')))):
						for k in range(head_id, len(heads)):
							if (check_belong_to(j, k, heads)):
								extension += ' ' + words[k]
				extension = extension[1:]
				###=== generate question ========================================================
				if (aux_id != -1):
					question = 'How many ' + noun + ' ' + words[aux_id] + ' ' + nsubj + ' ' + verb + ' ' + extension
				else:
					question = 'How many ' + noun + ' ' + nsubj + ' ' + verb + ' ' + extension
				if (xpos[head_id] == 'VBZ'):
					question = 'How many ' + noun + ' does ' + nsubj + ' ' + verb + ' ' + extension
				if (xpos[head_id] == 'VBP'):
					question = 'How many ' + noun + ' do ' + nsubj + ' ' + verb + ' ' + extension
				if (xpos[head_id] == 'VBD') and (aux_id == -1):
					question = 'How many ' + noun + ' did ' + nsubj + ' ' + verb + ' ' + extension
				answer = nummod + ' ' + noun

				###=== append ===================================================================
				questions.append(question + '?')
				answers.append(answer)
				relations.append('nummod')
		
		if (labels[i] == 'cop'):
			cop_id = i
			obj_id = heads[i]
			###=== get subject id ===============================================================
			subj_id = -1
			for j in range(1, len(heads)):
				if (heads[j] == obj_id) and (labels[j] in nsubj_labels):
					subj_id = j
			if (subj_id == -1):
				continue
			###=== check whether subject has nummod relation ====================================
			nummod_id = -1
			for j in range(1, len(heads)):
				if (labels[j] == 'nummod') and (heads[j] == subj_id):
					nummod_id = j
			"""
			=====================================================================================
			=== process sentences have form: (CD --nummod-- noun) + (be --cop-- noun) ===========
			=====================================================================================
			"""
			if (nummod_id != -1):
				###=== get nummod ===============================================================
				nummod = ''
				illegal_id = []
				for j in range(1, len(heads)):
					if (check_belong_to(nummod_id, j, heads)):
						nummod += ' ' + words[j]
						illegal_id.append(j)
				nummod = nummod[1:]
				###=== get subject ==============================================================
				subject = ''
				for j in range(1, len(heads)):
					if (j not in illegal_id) and (check_belong_to(subj_id, j, heads)):
						subject += ' ' + words[j]
				subject = subject[1:]
				###=== get tobe =================================================================
				tobe = ''
				for j in range(1, len(heads)):
					if (heads[j] == obj_id) and (labels[j] in ['cop', 'aux', 'auxpass']):
						tobe += ' ' + words[j]
				tobe = tobe[1:]
				###=== get dobject ==============================================================
				dobject = ''
				for j in range(1, len(heads)):
					if (j == obj_id):
						dobject += ' ' + words[j]
					if ((heads[j] == obj_id) and (labels[j] in ['compound', 'amod', 'nummod'])):
						for k in range(1, len(heads)):
							if (check_belong_to(j, k, heads)):
								dobject += ' ' + words[k]
				dobject = dobject[1:]
				###=== generate question ========================================================
				question = 'how many ' + subject + ' ' + tobe + ' ' + dobject
				answer = nummod

				###=== append ===================================================================
				questions.append(question + '?')
				answers.append(answer)
				relations.append('nummod')

			###=== check whether object has nummod relation ====================================
			nummod_id = -1
			for j in range(1, len(heads)):
				if (labels[j] == 'nummod') and (heads[j] == obj_id):
					nummod_id = j
			"""
			=====================================================================================
			=== process sentences have form: subject + (be --cop-- (CD --nummod-- noun)) ========
			=====================================================================================
			"""
			if (nummod_id != -1):
				###=== get nummod ===============================================================
				nummod = ''
				for j in range(1, len(heads)):
					if (check_belong_to(nummod_id, j, heads)):
						nummod += ' ' + words[j]
				nummod = nummod[1:]
				###=== get subject ==============================================================
				subject = ''
				for j in range(1, len(heads)):
					if (check_belong_to(subj_id, j, heads)):
						subject += ' ' + words[j]
				subject = subject[1:]
				###=== get tobe =================================================================
				tobe = ''
				for j in range(1, len(heads)):
					if (heads[j] == obj_id) and (labels[j] in ['cop', 'aux', 'auxpass']):
						tobe += ' ' + words[j]
				tobe = tobe[1:]
				###=== get dobject ==============================================================
				dobject = ''
				for j in range(1, len(heads)):
					if (j == obj_id):
						dobject += ' ' + words[j]
					if ((heads[j] == obj_id) and (labels[j] in ['compound'])):
						for k in range(1, len(heads)):
							if (check_belong_to(j, k, heads)):
								dobject += ' ' + words[k]
				dobject = dobject[1:]
				###=== generate question ========================================================
				question = 'how many ' + dobject + ' ' + tobe + ' ' + subject
				answer = nummod

				###=== append ===================================================================
				questions.append(question + '?')
				answers.append(answer)
				relations.append('nummod')
	### return
	return questions, answers, relations
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
		if (labels[i] == 'nummod') and (labels[heads[i]] in nsubj_labels) and (xpos[heads[heads[i]]] in verb_labels):
			nummod_id = i
			subj_id = heads[i]
			###=== get nummod ===================================================================
			nummod = ''
			for j in range(len(labels)):
				if check_belong_to(nummod_id, j, heads):
					nummod += ' ' + words[j]
			nummod = nummod[1:]
			###=== get subject and its compound =================================================
			noun = ''
			for j in range(1, len(heads)):
				if (j == subj_id) or ((heads[j] == subj_id) and (labels[j] == 'compound')):
					noun += ' ' + words[j]
			noun = noun[1:]
			###=== generate question ============================================================
			question_body = ''
			for j in range(1, len(heads)):
				if (not check_belong_to(subj_id, j, heads)) and (check_belong_to(heads[subj_id], j, heads)):
					if (words[j] == 'am'):
						question_body += ' is'
					else:
						question_body += ' ' + words[j]
			if (question_body == ''):
				continue
			question = 'How many ' + noun + ' ' + question_body
			###=== append =======================================================================
			questions.append(question + '?')
			answers.append(nummod + ' ' + noun)
			relations.append('nummod')

		"""
		=========================================================================================
		=== process sentences have form: subject + verb + direct_object(CD -- nummod -- noun) ===
		=========================================================================================
		"""
		if (labels[i] == 'nummod') and (labels[heads[i]] == 'dobj') and (xpos[heads[heads[i]]] in verb_labels):
			obj_id = heads[i]
			nummod_id = i
			verb_id = heads[obj_id]
			###=== check if exist nsubj point to head ==========================================
			nsubj_id = -1
			for j in range(1, len(labels)):
				if (check_belong_to(verb_id, j, heads) and (labels[j] in nsubj_labels)):
					nsubj_id = j
					break
			if (nsubj_id == -1):
				continue
			###=== get dobj info ================================================================
			is_human, type_noun = get_noun_info(words[obj_id], xpos[obj_id])
			if (ners[obj_id] == 'PERSON'):
				is_human = True
			for j in range(1, len(heads)):
				if (heads[j] == obj_id) and (labels[j] in ['conj']):
					noun_type = 1		
			###=== get body of question: the whole part belong to head except dobj ==============
			###=== get nsubject =================================================================
			nsubj = ''
			for j in range(1, len(heads)):
				if (check_belong_to(nsubj_id, j, heads)):
					nsubj += ' ' + words[j]
			nsubj = nsubj[1:]
			###=== get object and its compound =================================================
			noun = ''
			for j in range(1, len(heads)):
				if (j == obj_id) or ((heads[j] == obj_id) and (labels[j] == 'compound')):
					noun += ' ' + words[j]
			noun = noun[1:]
			###=== get nummod ===================================================================
			nummod = ''
			for j in range(len(heads)):
				if (check_belong_to(nummod_id, j, heads)):
					nummod += ' ' + words[j]
			nummod = nummod[1:]
			###=== get aux ======================================================================
			aux_id = -1
			for j in range(1, len(heads)):
				if (check_belong_to(verb_id, j, heads) and (labels[j] in ['aux', 'auxpass'])):
					aux_id = j
					break
			###=== get verb =====================================================================
			verb = ''
			for j in range(1, len(heads)):
				if (j == verb_id) or ((heads[j] == verb_id) and (j != aux_id) and (labels[j] in ['aux', 'auxpass'])):
					verb += ' ' + words[j]
			verb = verb[1:]
			###=== get extension ================================================================
			extension = ''
			for j in range(verb_id, len(heads)):
				if ((heads[j] == verb_id) and ((len(labels[j]) >= 4) and (labels[j][:4] == 'nmod'))):
					for k in range(verb_id, len(heads)):
						if (check_belong_to(j, k, heads)):
							extension += ' ' + words[k]
			extension = extension[1:]
			###=== generate question ============================================================
			if (aux_id != -1):
				question = 'How many ' + noun + ' ' + words[aux_id] + ' ' + nsubj + ' ' + verb + ' ' + extension
			else:
				question = 'How many ' + noun + ' ' + nsubj + ' ' + verb + ' ' + extension
			if (xpos[verb_id] == 'VBZ'):
				question = 'How many ' + noun + ' does ' + nsubj + ' ' + verb + ' ' + extension
			if (xpos[verb_id] == 'VBP'):
				question = 'How many ' + noun + ' do ' + nsubj + ' ' + verb + ' ' + extension
			if (xpos[verb_id] == 'VBD') and (aux_id == -1):
				question = 'How many ' + noun + ' did ' + nsubj + ' ' + verb + ' ' + extension
			answer = nummod + ' ' + noun
			###=== append =======================================================================
			questions.append(question + '?')
			answers.append(answer)
			relations.append('nummod')

		"""
		=========================================================================================
		=== process sentences have form: (CD --nummod-- noun) + (be --cop-- noun) ===============
		=========================================================================================
		"""
		if (labels[i] == 'nummod') and (labels[heads[i]] in nsubj_labels) and (xpos[heads[heads[i]]] in noun_labels):
			nummod_id = i
			subj_id = heads[i]
			obj_id = heads[subj_id]
			###=== check whether exist cop relation =============================================
			cop_id = -1
			for j in range(1, len(heads)):
				if (heads[j] == obj_id) and (labels[j] == 'cop'):
					cop_id = j
			if (cop_id == -1):
				continue
			###=== get nummod ===================================================================
			nummod = ''
			for j in range(1, len(heads)):
				if (check_belong_to(nummod_id, j, heads)):
					nummod += ' ' + words[j]
			nummod = nummod[1:]
			###=== get subject ==================================================================
			subject = ''
			for j in range(1, len(heads)):
				if (heads[j] == subj_id) and (labels[j] in ['compound', 'amod', 'det']):
					subject += ' ' + words[j]
			subject = subject[1:]
			###=== get tobe =====================================================================
			tobe = ''
			for j in range(1, len(heads)):
				if (heads[j] == obj_id) and (labels[j] in ['cop', 'aux', 'auxpass']):
					tobe += ' ' + words[j]
			tobe = tobe[1:]
			###=== get dobject ==================================================================
			dobject = ''
			for j in range(1, len(heads)):
				if (j == obj_id):
					dobject += ' ' + words[j]
				if ((heads[j] == obj_id) and (labels[j] in ['compound', 'amod', 'nummod'])):
					for k in range(1, len(heads)):
						if (check_belong_to(j, k, heads)):
							dobject += ' ' + words[k]
			dobject = dobject[1:]
			###=== generate question ============================================================
			question = 'how many ' + subject + ' ' + tobe + ' ' + dobject
			answer = nummod
		"""
		=========================================================================================
		=== process sentences have form: subject + (be --cop-- (CD --nummod-- noun)) ============
		=========================================================================================
		"""
		if (labels[i] == 'nummod') and (labels[heads[i]] == 'root'):
			nummod_id = i
			obj_id = heads[i]
			###=== get subject id ===============================================================
			subj_id = -1
			for j in range(1, len(heads)):
				if (heads[j] == obj_id) and (labels[j] in nsubj_labels):
					subj_id = j
			if (subj_id == -1):
				continue
			###=== get subject ==================================================================
			subject = ''
			for j in range(1, len(heads)):
				if (check_belong_to(subj_id, j, heads)):
					subject += ' ' + words[j]
			subject = subject[1:]
			###=== get tobe =====================================================================
			tobe = ''
			for j in range(1, len(heads)):
				if (heads[j] == obj_id) and (labels[j] in ['cop', 'aux', 'auxpass']):
					tobe += ' ' + words[j]
			tobe = tobe[1:]
			###=== get dobject ==================================================================
			dobject = ''
			for j in range(1, len(heads)):
				if (j == obj_id):
					dobject += ' ' + words[j]
				if ((heads[j] == obj_id) and (labels[j] in ['compound'])):
					for k in range(1, len(heads)):
						if (check_belong_to(j, k, heads)):
							dobject += ' ' + words[k]
			dobject = dobject[1:]
			###=== get nummod ===================================================================
			nummod = ''
			for j in range(1, len(heads)):
				if (check_belong_to(nummod_id, j, heads)):
					nummod += ' ' + words[j]
			nummod = nummod[1:]
			###=== generate question ============================================================
			question = 'how many ' + dobject + ' ' + tobe + ' ' + subject
			answer = nummod
			###=== append =======================================================================
			questions.append(question + '?')
			answers.append(answer)
			relations.append('nummod')
		"""
		=========================================================================================
		=== process sentences have form: ... + (verb --nmod:tmod-- (CD --nummod-- noun))=========
		=========================================================================================
		"""
		if (labels[i] == 'nummod') and (labels[heads[i]] in ['nmod:tmod']) and (xpos[heads[heads[i]]] in verb_labels):
			nummod_id = i
			verb_id = heads[heads[i]]
			illegal_id = []
			###=== get nummod ===================================================================
			nummod = ''
			for j in range(1, len(heads)):
				if (check_belong_to(nummod_id, j, heads)):
					nummod += ' ' + words[j]
					illegal_id.append(j)
			nummod = nummod[1:]
			###=== get noun and its compound ====================================================
			noun = ''
			for j in range(1, len(heads)):
				if (j == heads[i]) or ((heads[j] == heads[i]) and (labels[j] == 'compound')):
					noun += ' ' + words[j]
					illegal_id.append(j)
			noun = noun[1:]
			###=== get predicate ================================================================
			predicate = ''
			for j in range(1, len(heads)):
				if (j == verb_id):
					predicate += words[j]
				if (heads[j] == verb_id) and (labels[j] not in ['punct', 'aux']) and not ((len(labels[j]) >= 4) and (labels[j][:4] == 'nmod')):
					for k in range(1, len(heads)):
						if check_belong_to(j, k, heads):
							predicate += ' ' + words[k]
			predicate = predicate[1:]
			###=== generate question ============================================================
			if (xpos[verb_id] == 'VBZ'):
				question = 'how many ' + noun + ' does ' + predicate
			if (xpos[verb_id] == 'VBP'):
				question = 'how many ' + noun + ' do ' + predicate
			if (xpos[verb_id] == 'VBD'):
				question = 'how many ' + noun + ' did ' + predicate
			if (xpos[verb_id] == 'VBN'):
				question = 'how many ' + noun + ' have ' + predicate
			answer = nummod
			###=== append =======================================================================
			questions.append(question + '?')
			answers.append(answer)
			relations.append('nummod')

	### return
	return questions, answers, relations
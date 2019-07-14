
from .extended_function import check_belong_to, get_noun_info

def generate_nmod_question(words, xpos, heads, labels, ners):
	###
	questions = []
	answers = []
	relations = []
	verb_labels = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
	adj_labels = ['JJ', 'JJR', 'JJS']
	noun_labels = ['NN', 'NNP', 'NNS', 'NNPS']
	nsubj_labels = ['nsubj', 'nsubjpass']
	nmod_labels = ['nmod:in', 'nmod:on', 'nmod:at', 'nmod:before', 'nmod:after', 'nmod:near']
	"""
		nmod:in -> location
	"""
	for i in range(1, len(labels)):
		"""
			process sentences have form: subject + verb + in/on + TIME/LOCATION
		"""
		if (labels[i] in ['nmod:in', 'nmod:on']) and (xpos[heads[i]] in verb_labels) and (ners[i] in ['TIME', 'DATE', 'LOCATION', 'ORGANIZATION']):
			entity_id = i
			verb_id = heads[i]
			subj_id = -1
			###============== get subj id =======================================================
			for j in range(1, len(heads)):
				if (heads[j] == verb_id) and (labels[j] in nsubj_labels):
					subj_id = j
			###=== only process sentence in form subj + verb + in + location ====================
			if (subj_id == -1):
				continue
			###=== exist auxulary or not ========================================================
			first_aux = -1
			for j in range(1, len(heads)):
				if (heads[j] == verb_id) and (labels[j] in ['aux', 'auxpass']):
					first_aux = j
					break
			###=== get subject ==================================================================
			subj = ''
			for j in range(1, len(heads)):
				if (check_belong_to(subj_id, j, heads)):
					subj += ' ' + words[j]
			subj = subj[1:]
			###=== get verb =====================================================================
			illegal_id = []
			verb = ''
			for j in range(1, len(heads)):
				if (heads[j] == verb_id) and ((labels[j] in nsubj_labels + nmod_labels + ['case', 'det', 'prep', 'mark', 'punct', 'ccomp', 'acl', 'acl:relcl', 'cop']) or (((len(labels[j]) >= 5) and (labels[j][:5] == 'advcl')))):
					for k in range(1, len(heads)):
						if (check_belong_to(j, k, heads)):
							illegal_id.append(k)
			for j in range(1, len(heads)):
				if (j != first_aux) and (j not in illegal_id) and (check_belong_to(verb_id, j, heads)):
					verb += ' ' + words[j]
			verb = verb[1:]
			###=== get entity ==================================================================
			entity = ''
			for j in range(1, len(heads)):
				if (j == entity_id):
					entity += ' ' + words[j]
				if (heads[j] == entity_id) and (labels[j] in ['compound', 'nummod']):
					for k in range(1, len(heads)):
						if (check_belong_to(j, k ,heads)):
							entity += ' ' + words[k]
			entity = entity[1:]
			###=== generate question ===========================================================
			question = ''
			answer = ''
			if (ners[i] == 'LOCATION') or (ners[i] == 'ORGANIZATION'):
				if (first_aux == -1):
					if (xpos[verb_id] == 'VBZ'):
						question = 'where does'
					if (xpos[verb_id] == 'VBP'):
						question = 'where do'
					if (xpos[verb_id] == 'VBD'):
						question = 'where did'
				else:
					question = 'where ' + words[first_aux]

			if (ners[i] == 'DATE') or (ners[i] == 'TIME'):
				if (first_aux == -1):
					if (xpos[verb_id] == 'VBZ'):
						question = 'when does'
					if (xpos[verb_id] == 'VBP'):
						question = 'when do'
					if (xpos[verb_id] == 'VBD'):
						question = 'when did'
				else:
					question = 'when ' + words[first_aux]

			question += ' ' + subj + ' ' + verb
			answer = entity
			questions.append(question)
			answers.append(answer)
			relations.append('nmod')

		"""
			process sentences have form: subject + verb + dobj + in/on + TIME/LOCATION
		"""
		if (labels[i] in ['nmod:in', 'nmod:on']) and (ners[i] in ['TIME', 'DATE', 'LOCATION', 'ORGANIZATION']):
			###=== check whether word[i] has relative with a dobj label
			dobj_id = -1
			for j in range(1, len(heads)):
				if (labels[j] == 'dobj') and (check_belong_to(j, i, heads)):
					dobj_id = j
			if (dobj_id == -1):
				continue
			###=== get subject_id, verb_id ======================================================
			subj_id = -1
			verb_id = -1
			if (xpos[heads[dobj_id]] in verb_labels):
				verb_id = heads[dobj_id]
			for j in range(1, len(heads)):
				if (heads[j] == verb_id) and (labels[j] in nsubj_labels):
					subj_id = j
			if (subj_id == -1) or (verb_id == -1):
				continue
			###=== exist auxulary or not ========================================================
			first_aux = -1
			for j in range(1, len(heads)):
				if (heads[j] == verb_id) and (labels[j] in ['aux', 'auxpass']):
					first_aux = j
					break
			###=== get subject ==================================================================
			subj = ''
			for j in range(1, len(heads)):
				if (check_belong_to(subj_id, j, heads)):
					subj += ' ' + words[j]
			subj = subj[1:]
			###=== get verb =====================================================================
			illegal_id = []
			verb = ''
			for j in range(1, len(heads)):
				if (heads[j] == verb_id) and (labels[j] in nsubj_labels + nmod_labels + ['case', 'det', 'prep', 'mark', 'punct', 'xcomp', 'acl', 'acl:relcl', 'cop', 'dobj']):
					for k in range(1, len(heads)):
						if (check_belong_to(j, k, heads)):
							illegal_id.append(k)
			for j in range(1, len(heads)):
				if (j != first_aux) and (j not in illegal_id) and (check_belong_to(verb_id, j, heads)):
					verb += ' ' + words[j]
			verb = verb[1:]
			###=== get entity ===================================================================
			entity_id = i
			entity = ''
			for j in range(1, len(heads)):
				if (j == entity_id):
					entity += ' ' + words[j]
				if (heads[j] == entity_id) and (labels[j] in ['compound', 'nummod']):
					for k in range(1, len(heads)):
						if (check_belong_to(j, k ,heads)):
							entity += ' ' + words[k]
			entity = entity[1:]
			###=== get direct object ===========================================================
			dobject = ''
			for j in range(1, len(heads)):
				if (not check_belong_to(entity_id, j, heads)) and (check_belong_to(dobj_id, j, heads)):
					dobject += ' ' + words[j]
			dobject = dobject[1:]
			###=== generate question ===========================================================
			question = ''
			answer = ''
			if (ners[i] == 'LOCATION') or (ners[i] == 'ORGANIZATION'):
				if (first_aux == -1):
					if (xpos[verb_id] == 'VBZ'):
						question = 'where does'
					if (xpos[verb_id] == 'VBP'):
						question = 'where do'
					if (xpos[verb_id] == 'VBD'):
						question = 'where did'
				else:
					question = 'where ' + words[first_aux]

			if (ners[i] == 'DATE') or (ners[i] == 'TIME'):
				if (first_aux == -1):
					if (xpos[verb_id] == 'VBZ'):
						question = 'when does'
					if (xpos[verb_id] == 'VBP'):
						question = 'when do'
					if (xpos[verb_id] == 'VBD'):
						question = 'when did'
				else:
					question = 'when ' + words[first_aux]

			question += ' ' + subj + ' ' + verb + ' ' + dobject
			answer = entity
			questions.append(question)
			answers.append(answer)
			relations.append('nmod')

	return questions, answers, relations





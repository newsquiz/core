from nltk.corpus import wordnet as wn

def check_belong_to(i, j, heads):
	cnt = 0
	while (j != 0) and (j != i):
		j = heads[j]
		cnt += 1
		if (cnt == 100):
			return False
	if (j == i):
		return True
	else:
		return False


def get_all_word_belong_to(i, words, heads):
	answer = ''
	last_answer_id = -1
	for j in range(1, len(heads)):
		if check_belong_to(i, j, heads):
			answer += ' ' + words[j]
			last_answer_id = j
	return answer, last_answer_id


def get_noun_info(noun, tag):
	noun_labels = ['NN', 'NNP', 'NNS', 'NNPS']
	personal_pronoun_labels = ['PRP']
	singular_personal_pronoun = ['i', 'she', 'he', 'it']
	plural_personal_pronoun = ['we', 'you', 'they']
	### noun type is singular (0) or prural (1)
	noun_type = 0
	is_human = False
	if (tag in noun_labels):
		if (tag in ['NNS', 'NNPS']):
			noun_type = 1

		### noun points to Human or not
		synsets = wn.synsets(str(wn.morphy(noun.lower())), 'n')
		if (len(synsets) != 0):
			cnt = 0
			noun = synsets[0]
			while (len(noun.hypernyms()) != 0) and (cnt < 100):
				cnt += 1
				if (noun.name()[:6] == 'person'):
					is_human = True
					break
				noun = noun.hypernyms()[0]
	if (tag in personal_pronoun_labels + plural_personal_pronoun):
		if (noun.lower() in plural_personal_pronoun):
			noun_type = 1
		if (noun.lower() in ['i', 'we', 'she', 'he', 'you', 'they']):
			is_human = True

	### return
	return is_human, noun_type
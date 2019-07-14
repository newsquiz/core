from nltk.corpus import wordnet as wn 
from nltk.wsd import lesk

def synonym_paraphrase(words, xpos):
	verb_labels = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
	adj_labels = ['JJ', 'JJR', 'JJS']
	noun_labels = ['NN', 'NNP', 'NNS', 'NNPS']
	adv_labels = ['RB', 'RBR', 'RBS']
	synonyms = {}
	for i in range(len(words)):
		### get pos tag
		pos_tag = None
		if (xpos[i] in verb_labels):
			pos_tag = 'v'
		if (xpos[i] in adj_labels):
			pos_tag = 'a'
		if (xpos[i] in noun_labels):
			pos_tag = 'n'
		if (xpos[i] in adv_labels):
			pos_tag = 'r'
		if (pos_tag == None):
			continue
		### get morphy of word
		morphy = wn.morphy(words[i], pos_tag)
		if (morphy == None):
			continue
		### get all synonyms
		meaning = lesk(' '.join(words), morphy, pos_tag)
		if (str(meaning) == 'None'):
			continue
		syns = meaning.lemma_names()
		synonyms[morphy] = syns

	return synonyms

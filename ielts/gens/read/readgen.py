from ..base import QuestionGenerator
from enlp import DependencyParser, POS, SentenceTokenizer, NER
from .generate_question import generate_question
from .paraphrase.paraphrase import Paraphrase
from ...utils import DocumentGraph


class ReadGen(QuestionGenerator):
    '''Reading questin generator.'''
    
    def __init__(self, crawler):
        #put more required models for initilizing the generator
        super(ReadGen, self).__init__()
        self.crawler = crawler
        self.dependparser = DependencyParser()
        self.pos = POS()
        self.ner = NER()
        self.sen_tokenizer = SentenceTokenizer()
        self.paraphrase = Paraphrase(self.pos, self.dependparser)

    def fit(self):
        '''Fit or reload prediction model.'''
        pass

    def predict(self, request_body):
        '''Predict a list of questions for the docment.

        Args:
            - request_body: a dict contains either key 'text' or 'url' and other information for the request

        Returns:
            - error: if there is an error during generation
            - questions: A list of question instances that have been defined in common/question.py
        '''
        if 'text' in request_body:
            text = request_body['text']
            return None, self.transform(text)
        elif 'url' in request_body:
            url = request_body['url']
            text = self.crawler.get_text(url)
            return None, self.transform(text)
        else:
            return Errors.INVALID_REQUEST, None


    def transform(self, text):
        sentences = self.sen_tokenizer.transform(text)
        print(sentences)
        docgraph = DocumentGraph(text)
        res = []
        for i in range(len(sentences)):
            entities = []

            print('process root sentence')
            print('get paraphrase...')
            paraphrases = self.paraphrase.transform(sentences[i])
            _res = {'generate_question' : [], 'synonyms' : []}
            print('generate questions...')
            for para in paraphrases['sentence_paraphrases']:
                print(para)
                _res['generate_question'].append({'text' : para, 'question' : generate_question(para, self.dependparser, self.pos, self.ner, entities)})
            # _res['synonyms'] = paraphrases['word_paraphrases']
            res.append(_res)

            print('process name entity sentences')
            print('replace all entity...')
            for e in docgraph.get_sentence_entities(i):
                if (e.refer == None):
                    continue
                while (e.refer.refer != None):
                    e.refer = e.refer.refer
                sentences[i] = sentences[i].replace(e.text, e.refer.text, 1)
                entities.append(e.refer.text)
            print('get paraphrase...')
            paraphrases = self.paraphrase.transform(sentences[i])
            _res = {'generate_question' : [], 'synonyms' : []}
            print('generate questions...')
            for para in paraphrases['sentence_paraphrases']:
                _res['generate_question'].append({'text' : para, 'question' : generate_question(para, self.dependparser, self.pos, self.ner, entities)})
            # _res['synonyms'] = paraphrases['word_paraphrases']
            res.append(_res)
        return res

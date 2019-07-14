from collections import defaultdict
from ..base import QuestionGenerator
from ielts.errors import Errors
from enlp import NER, POS, DependencyParser, Coreference, SentenceTokenizer, WordTokenizer
from ielts.utils import DocumentGraph
from ielts.common import Entity

import pdb


class ListenGen(QuestionGenerator):
    '''Reading questin generator.'''
    
    def __init__(self, crawler):
        #put more required models for initilizing the generator
        super(ListenGen, self).__init__()
        self.crawler = crawler

    def fit(self):
        '''Fit or reload prediction model.'''
        pass

    def transform(self, text):
        dgraph = DocumentGraph(text)
        return None, []

    def predict(self, request_body):
        '''Predict a list of questions for the document.

        Args:
            - request_body: a dict contains information for the request

        Returns:
            - error: if the is an error during generation
            - questions: A list of question instances that have been defined in common/question.py
        '''
        if 'text' in request_body:
            text = request_body['text']
            return self.transform(text)
        elif 'url' in request_body:
            url = request_body['url']
            text = self.crawler.get_text(url)
            return self.transform(text)
        else:
            return Errors.INVALID_REQUEST, None 

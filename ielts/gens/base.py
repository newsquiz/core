from logging import getLogger

class QuestionGenerator(object):
    
    def __init__(self):
        #put more required models for initilizing the generator
        self.logger = getLogger('gens')

    def fit(self):
        '''Fit or reload prediction model.'''
        pass

    def predict(self, request_body):
        '''Find out most potential questions from text in request body

        Args:
            request_body: a dict which has the key either 'text' or 'url'

        Returns:
            - error: if the is an error during generation
            - questions: A list of question instances that have been defined in common/question.py
        '''
        pass

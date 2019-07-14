from logging import getLogger

class SkillEvaluator(object):

    def __init__(self):
        #put more required models for initilizing the evaluator
        self.logger = getLogger('evals')

    def fit(self):
        '''Fit or reload predition model.'''
        pass

    def predict(self, question):
        '''Evaluate the given question.
        
        Args:
            question: is an appropriate instance of question classes defined in commont/question.py. It also contains user's answers.

        Return: A tuple contains:
            error: If the quetions is not the right type for the Evaluator, and other
            predictions: Prediction of the evaluator
            feedback: if possible, for improve score
            
        '''
        pass
    
    

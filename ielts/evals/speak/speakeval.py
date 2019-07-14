from ..base import SkillEvaluator

class SpeakEval(SkillEvaluator):

    def __init__(self):
        #put more required models for initilizing the evaluator
        super(SpeakEval, self).__init__()

    def fit(self):
        '''Fit or reload predition model.'''
        pass

    def predict(self, question):
        '''Questions is an instance of SpeakQuestion which was enclosed with user's answer.

        Return: A tuple contains:
            - error: If the quetions is not the right type for the Evaluator, and other
            - predictions: Prediction of the evaluator
            - feedback: if possible, for improve score
            
        '''
        pass
    
    

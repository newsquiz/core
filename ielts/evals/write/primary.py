from ..base import SkillEvaluator


class WriteEval(SkillEvaluator):
    def __init__(self, *evaluators, weights=None):
        # put more required models for initilizing the evaluator
        super(WriteEval, self).__init__()
        self.evaluators = evaluators

        if weights is None:
            self.weights = [1.0] * len(evaluators)
        else:
            assert (len(weights) == len(evaluators))
            self.weights = weights

    def fit(self):
        """Fit or reload prediction model."""
        for ev in self.evaluators:
            ev.fit()

    def predict(self, questions):
        """
        Question may be an object common/question.py or a list of them.
        Each question contains its question and user's answers.

        Return: A tuple contains:
            - error: If the quetions is not the right type for the Evaluator, and other
            - predictions: Prediction of the evaluator
            - feedback: if possible, for improve score

        """
        if isinstance(questions, (list, tuple)):
            predictions, feedbacks = [], []
            for q in questions:
                err, pred, fb = self.predict(q)
                if err is not None:
                    return err, None, None
                predictions.append(pred)
                feedbacks.append(fb)
            return None, predictions, feedbacks
        else:
            total, feedbacks = 0.0, []
            for i, ev in enumerate(self.evaluators):
                err, pred, fb = ev.predict(questions)
                if err is not None:
                    return err, None, None
                total += pred * self.weights[i]
                feedbacks.append(fb)
            score = total / sum(self.weights)
            return None, score, feedbacks

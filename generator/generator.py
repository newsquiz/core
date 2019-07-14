from enlp import DependencyParser, POS, SentenceTokenizer, NER, Coreference
from .generate_question import generate_question_QA, generate_question_4FF, generate_question_FF
from .paraphrase.paraphrase import Paraphrase
import random
import pdb

class QuestionGenerator(object):
    '''Reading questin generator.'''
    
    def __init__(self):
        #put more required models for initilizing the generator
        self.dependparser = DependencyParser()
        self.pos = POS()
        self.ner = NER()
        self.sen_tokenizer = SentenceTokenizer()
        self.paraphrase = Paraphrase(self.pos, self.dependparser)
        self.coreference = Coreference()


    def gen_QA(self, sentences):
        res = []
        for i in range(len(sentences)):
            entities = []
            print('process root sentence')
            print('get paraphrase...')
            # paraphrases = self.paraphrase.transform(sentences[i])
            # print('generate questions...')
            # for para in paraphrases['sentence_paraphrases']:
            for para in [sentences[i]]:
                res += generate_question_QA(para, self.dependparser, self.pos, self.ner, entities)
        res_question = ""
        res_answer = ""
        res_rank = 0
        for r in res:
            rank = r["rank"]
            question = r["question"]
            answer = r["answer"]
            if (rank > res_rank) or ((rank == res_rank) and (len(question) > len(res_question))):
                    res_question = question
                    res_rank = rank
                    res_answer = answer
        return (res_question, res_answer)


    def gen_4FF(self, sentences):
        """
        choose word of type
        Noun: 
        Verb:
        Adj :
        """
        res = generate_question_4FF(sentences, self.dependparser, self.pos, self.ner)
        if res[0] == None:
            return res[1]
        elif res[1] == None:
            return res[0]
        return res[random.choice([0, 1])]


    def gen_FF(self, sentences):
        """
        choose word of type
        Noun: 
        Verb:
        Adj :
        """
        res = generate_question_FF(sentences, self.dependparser, self.pos, self.ner)
        idxs = []
        for i in range(len(res)):
            if res[i] != None:
                idxs.append(i)
        if len(idxs) == 0:
            return None
        return res[random.choice(idxs)]


    def transform(self, text):
        """
        TODO
            process name entity sentences
            replace all entity
        """
        sentences = self.sen_tokenizer.transform(text)
        res = []
        print("generate QA question")
        QA_question = self.gen_QA(sentences)
        res.append(("QA", QA_question))
        print("generate 4FF question")
        FF4_question = self.gen_4FF(sentences)
        res.append(("FF4", FF4_question))
        print("generate FF question")
        FF_question  = self.gen_FF(sentences)
        res.append(("FF", FF_question))
        return res

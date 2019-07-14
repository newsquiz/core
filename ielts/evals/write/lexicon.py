from nltk.corpus.reader import BNCCorpusReader

from ..base import SkillEvaluator


class LexiconEvaluator(SkillEvaluator):
    def __init__(self):
        super().__init__()
        self._lexicon = None

    def fit(self, lexicon_cls=BncLexicon, lexicon_path=None, **lexicon_args):
        if lexicon_path is not None:
            self._lexicon = lexicon_cls.load(lexicon_path)
        else:
            self._lexicon = lexicon_cls(**lexicon_args)
            self._lexicon.build()

    def predict(self, questions):
        pass


class FrequencyLexicon:
    def __init__(self):
        pass

    def __getitem__(self, item):
        pass

    def __setitem__(self, key, value):
        pass

    def get(self, item, default=None):
        try:
            return self[item]
        except KeyError:
            return default

    def build(self, limit=None):
        pass

    def save(self, path, **kwargs):
        pass

    @classmethod
    def load(cls, path):
        pass


class BncLexicon(FrequencyLexicon):
    def __init__(self, root=None):
        super().__init__()
        self.root = root
        self._dict = {}

    def __getitem__(self, item):
        return self._dict[item]

    def __setitem__(self, key, value):
        self._dict[key] = value

    def build(self, limit=None):
        fileids = r'[A-K]/\w*/\w*\.xml'
        reader = BNCCorpusReader(self.root, fileids)
        temp_dict = {}
        for word, pos in reader.tagged_words(fileids, stem=True):
            key = (word, pos)
            temp_dict[key] = 0 if key in temp_dict else temp_dict[key] + 1

        sorted_items = sorted(temp_dict.items(), key=lambda x: x[1])

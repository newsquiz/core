import re
import os
import sys
import json
import math
import string
import operator
from collections import defaultdict
from collections import OrderedDict

import nltk
#nltk.download("punkt")
#nltk.download("stopwords")
#nltk.download("averaged_perceptron_taggepython r")

import argparse
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.externals import joblib

import aqg.utils.linguistic as ling
from aqg.utils.file_reader import File_Reader
from aqg.utils.file_writer import File_Writer
from aqg.utils.sentence_selection import SentenceSelection

class SentenceSelector(object):
	def __init__(self):
		self.ss = SentenceSelection()

	def transform(self, doc):
		sentences = self.ss.prepare_sentences_from_rawtext(doc)
		return sentences
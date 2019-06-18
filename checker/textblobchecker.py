from textblob import TextBlob,Word

from .base import BaseChecker

class TextBlobChecker(BaseChecker):
	"""TextBlobChecker uses primitive algorithm using textblob"""
	def __init__(self, preproc_rules=None):
		super(TextBlobChecker, self).__init__(preproc_rules)

	def process(self,sent):
		w=Word(sent)		
		return [max(w.spellcheck(), key=lambda x:x[1])][0]

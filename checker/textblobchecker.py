from textblob import TextBlob,Word

from .base import BaseChecker

class TextBlobChecker(BaseChecker):
	"""docstring for TextBlobChecker"""
	def __init__(self, preproc_rules=None):
		super(TextBlobChecker, self).__init__(preproc_rules)
		self.opt=2

	def process(self,sent):
		w=Word(sent)		
		return [max(w.spellcheck(), key=lambda x:x[1])][0]

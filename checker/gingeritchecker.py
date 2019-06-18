from gingerit.gingerit import GingerIt

from .base import BaseChecker

class GingerItChecker(BaseChecker):
	"""GingerItChecker uses Ginger API for spell correction"""
	def __init__(self, preproc_rules=None):
		super(GingerItChecker, self).__init__(preproc_rules)
		
	def process(self,sent):
		parser=GingerIt()
		res=parser.parse(sent)
		correct_spells=[]
		return res['result'].split(" ")



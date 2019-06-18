from gingerit.gingerit import GingerIt

from .base import BaseChecker

class GingerItChecker(BaseChecker):
	"""docstring for GingerItChecker"""
	def __init__(self, preproc_rules=None):
		super(GingerItChecker, self).__init__(preproc_rules)
		
		self.opt=2

	def process(self,sent):
		parser=GingerIt()
		res=parser.parse(sent)
		correct_spells=[]
		
		if self.opt==1:
			for corr in res['corrections']:
				correct_spells.extend(corr['correct'].split(" "))
		else:
			return res['result'].split(" ")
		
		return correct_spells



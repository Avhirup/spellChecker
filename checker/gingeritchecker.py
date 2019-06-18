from gingerit.gingerit import GingerIt

from .base import BaseChecker

class GingerItChecker(BaseChecker):
	"""docstring for GingerItChecker"""
	def __init__(self, preproc_rules=None):
		super(GingerItChecker, self).__init__(preproc_rules)
		
		self.opt=2

	def process(self,sent):
		parser=GingerIt()
		print(111)
		res=parser.parse(sent)
		print(1111)
		correct_spells=[]
		
		if self.opt==1:
			for corr in res['corrections']:
				correct_spells.extend(corr['correct'].split(" "))
		else:
			return res['result'].split(" ")
		print(correct_spells)
		return correct_spells



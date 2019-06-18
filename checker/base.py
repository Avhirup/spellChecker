import logging
import abc
import re

class BaseChecker(metaclass=abc.ABCMeta):
	"""Base class for all Checker methods"""
	def __init__(self, preproc_rules=None):
		super(BaseChecker, self).__init__()
		self.preproc_rules = preproc_rules

	@abc.abstractmethod
	def process(self,res):
		"""
		formats result		
		"""

	def checks_spell(self,sent):
		sent=self.preproc_rules.transform(sent)
		res=self.process(sent)
		return res
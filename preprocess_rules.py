import re
import logging
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.pipeline import Pipeline
logger=logging.getLogger(__name__)

class Rule(BaseEstimator,TransformerMixin):
	"""docstring for Rule"""
	def fit(self,X,y=None):
		return self

	def transform(self,X,y=None):
		return self.process(X)

	def process(self,sent):
		raise NotImplementedError("Cant use base class method. Please initiate")


class RemoveNonAlphanumeric(Rule):
	"""docstring for RemoveNonAlphanumeric"""
	name="RemoveNonAlphanumeric"
	def process(self,sent):
		return re.sub('[^\w.,;!?]', '',sent)
		# return re.sub('[\W]', '',sent)

rule_pipe=Pipeline([("RemoveNonAlphanumeric",RemoveNonAlphanumeric())])

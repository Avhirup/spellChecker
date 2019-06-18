import re
import logging
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.pipeline import Pipeline
logger=logging.getLogger(__name__)

class Rule(BaseEstimator,TransformerMixin):
	"""Base class to implement any rule for processing"""
	def fit(self,X,y=None):
		return self

	def transform(self,X,y=None):
		return self.process(X)

	def process(self,sent):
		raise NotImplementedError("Cant use base class method. Please initiate")


class RemoveNonAlphanumeric(Rule):
	"""RemoveNonAlphanumeric"""
	name="RemoveNonAlphanumeric"
	def process(self,sent):
		return re.sub('[^\w.,;!?]', '',sent)

rule_pipe=Pipeline([("RemoveNonAlphanumeric",RemoveNonAlphanumeric())])

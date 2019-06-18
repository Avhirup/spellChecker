import re
import numpy as np
from collections import Counter
from utils import words
from .base import BaseChecker
from memo import memo
from functools import reduce
from textblob import Word

class SpellCorrector(object):
	"""docstring for SpellCorrector"""
	def __init__(self, corpus_path='big.txt'):
		super(SpellCorrector, self).__init__()
		self.Words = dict(Counter(words(open(corpus_path).read())))
		self.N=sum(self.Words.values())

			
	def P(self,word): 
		"Probability of `word`."
		try:
			return self.Words[word] / self.N        
		except KeyError:
			#prob for word not found is extremely low 
			return -np.inf
	
	def correction(self,word): 
		"Most probable spelling correction for word."
		# return list(map(lambda x: (x,self.P(x)),self.candidates(word)))
		return max(self.candidates(word), key=self.P)

		
	def candidates(self,word): 
		"Generate possible spelling corrections for word."
		return self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word]
		# return self.known([word]) + self.known(self.edits1(word)) + self.known(self.edits2(word)) + [word]
			
	def known(self,words): 
		"The subset of `words` that appear in the dictionary of Words."
		return (set(w for w in words if w in self.Words))

	def edits1(self,word):
		"All edits that are one edit away from `word`."
		letters    = 'abcdefghijklmnopqrstuvwxyz -'
		splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
		deletes    = [L + R[1:]               for L, R in splits if R]
		transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
		replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
		inserts    = [L + c + R               for L, R in splits for c in letters]
		return set(deletes + transposes + replaces + inserts)

	def edits2(self,word): 
		"All edits that are two edits away from `word`."
		return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))
		

class WordSegmentor(object):
	"""docstring for WordSegmentor"""
	def __init__(self, corpus_path='big.txt',use_textblob=False):
		super(WordSegmentor, self).__init__()
		self.sc=SpellCorrector(corpus_path)
		self.WORDS = Counter(words(open(corpus_path).read()))
		self.max_word_length = max(map(len, self.WORDS))
		self.total = float(sum(self.WORDS.values()))
		self.use_textblob=use_textblob

	def splits(self,text, L=5):
		"Return a list of all possible (first, rem) pairs, len(first)<=L."
		splitsa =  [(text[:i+1], text[i+1:]) for i in range(max(len(text), L))]
		return splitsa

	@memo
	def segment(self,text):
		"Return a list of words that is the best segmentation of text."
		if not text: return []
		candidates = [[first]+[rem] for first,rem in self.splits(text)]
		print(list(candidates))
		print(list(map(lambda x: (x,self.Pwords(x)),candidates)))
		return max(candidates, key=self.Pwords)
	
	def Pwords(self,words):
		"The Naive Bayes probability of a sequence of words."
		prod = 0.0
		prod =  reduce(lambda a,b:a*b,(self.word_prob(self.sc.correction(w)) for w in words))
		return prod

	def word_prob(self,word):
		if not self.use_textblob:
			return self.WORDS[word] / self.total
		else:
			#need to improve this spell check is giving w
			return Word(word).spellcheck()[0][1]

		
class ScratchChecker(BaseChecker):
	"""docstring for ScratchChecker"""
	def __init__(self, preproc_rules=None,file_path='big.txt'):
		super(ScratchChecker, self).__init__(preproc_rules)
		self.sc=SpellCorrector(file_path)
		self.ws=WordSegmentor(file_path)
		self.WORDS = dict(Counter(words(open(file_path).read())))

	def process(self,word):
		out =  self.ws.segment(word)
		output = []
		for o in range(len(out)):
			output.append(self.sc.correction(out[o]))
		# print(out)
		return output

		

		

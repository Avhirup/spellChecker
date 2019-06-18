import numpy as np
import spacy
import re
import string
import argparse
import pandas as pd
from nltk.corpus import stopwords
import nltk
from collections import Counter,defaultdict
import pickle as pkl 
from utils import removeNonAscii,clean_comments,words
#get english stopwords
en_stopwords = set(stopwords.words('english'))

argparser = argparse.ArgumentParser(description='Spelling Correction app')
argparser.add_argument('--corpus_path', default="big.txt")
args = argparser.parse_args()

comments = open(args.corpus_path,'r').read()
THRESHOLD_FREQ=2
THRES=4

#function to filter for ADJ/NN bigrams
def rightTypes(ngram):
    if '-pron-' in ngram or 't' in ngram:
        return False
    for word in ngram:
        if word in en_stopwords or word.isspace():
            return False
    acceptable_types = ('JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS')
    second_type = ('NN', 'NNS', 'NNP', 'NNPS')
    tags = nltk.pos_tag(ngram)
    if tags[0][1] in acceptable_types and tags[1][1] in second_type:
        return True
    else:
        return False

#function to filter for trigrams
def rightTypesTri(ngram):
    if '-pron-' in ngram or 't' in ngram:
        return False
    for word in ngram:
        if word in en_stopwords or word.isspace():
            return False
    first_type = ('JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS')
    third_type = ('JJ', 'JJR', 'JJS', 'NN', 'NNS', 'NNP', 'NNPS')
    tags = nltk.pos_tag(ngram)
    if tags[0][1] in first_type and tags[2][1] in third_type:
        return True
    else:
        return False

#function to remove non-ascii characters
comments =  removeNonAscii(comments)
comments=clean_comments(comments)

bigrams = nltk.collocations.BigramAssocMeasures()
trigrams = nltk.collocations.TrigramAssocMeasures()

bigramFinder = nltk.collocations.BigramCollocationFinder.from_words(comments)
trigramFinder = nltk.collocations.TrigramCollocationFinder.from_words(comments)

#bigrams
bigram_freq = bigramFinder.ngram_fd.items()
bigramFreqTable = pd.DataFrame(list(bigram_freq), columns=['bigram','freq']).sort_values(by='freq', ascending=False)

#trigrams
trigram_freq = trigramFinder.ngram_fd.items()
trigramFreqTable = pd.DataFrame(list(trigram_freq), columns=['trigram','freq']).sort_values(by='freq', ascending=False)

#filter
filtered_bi = bigramFreqTable[bigramFreqTable.bigram.map(lambda x: rightTypes(x))]
filtered_tri = trigramFreqTable[trigramFreqTable.trigram.map(lambda x: rightTypesTri(x))]

#filter for only those with more than 20 occurences
bigramFinder.apply_freq_filter(THRESHOLD_FREQ)
trigramFinder.apply_freq_filter(THRESHOLD_FREQ)

bigramPMITable = pd.DataFrame(list(bigramFinder.score_ngrams(bigrams.pmi)), columns=['bigram','PMI']).sort_values(by='PMI', ascending=False)
trigramPMITable = pd.DataFrame(list(trigramFinder.score_ngrams(trigrams.pmi)), columns=['trigram','PMI']).sort_values(by='PMI', ascending=False)


bigramPMITable=bigramPMITable[bigramPMITable.PMI>THRES]
bigramPMITable.bigram=bigramPMITable.bigram.apply(lambda x:" ".join(x))
bigramFreqTable.bigram=bigramFreqTable.bigram.apply(lambda x:" ".join(x))
bigramFreqTable=bigramFreqTable[bigramFreqTable.bigram.isin(bigramPMITable.bigram.tolist())].to_dict('list')
bigrams={}

for k,v in zip(bigramFreqTable['bigram'],bigramFreqTable['freq']):
    bigrams[k]=v

trigramPMITable=trigramPMITable[trigramPMITable.PMI>THRES]
trigramPMITable.trigram=trigramPMITable.trigram.apply(lambda x:" ".join(x))
trigramFreqTable.trigram=trigramFreqTable.trigram.apply(lambda x:" ".join(x))
trigramFreqTable=trigramFreqTable[trigramFreqTable.trigram.isin(trigramPMITable.trigram.tolist())].to_dict('list')
trigrams={}

for k,v in zip(trigramFreqTable['trigram'],trigramFreqTable['freq']):
    trigrams[k]=v

words_counter=dict(Counter(words(open(args.corpus_path).read())))


with open("WORDS.pkl","wb") as f:
    pkl.dump({**words_counter,**bigrams,**trigrams},f)
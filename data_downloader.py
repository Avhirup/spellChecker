from google_ngram_downloader import readline_google_store
from collections import defaultdict
import re
import pdb

COUNT=1000000
counter = defaultdict(int)

for n_gram in range(2,6):
	fname, url, records = next(readline_google_store(ngram_len=n_gram))
	i=0
	while len(counter.keys())<COUNT:
		ng=next(records)
		x=re.sub('^[\w ]','',ng.ngram).split("_")[0]
		counter[x]+=ng.match_count
		i+=1
	pdb.set_trace()

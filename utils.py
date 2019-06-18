import logging
from datetime import datetime
import re
from collections import Counter
import spacy
import string 
nlp = spacy.load('en')

_LOGGER = logging.getLogger('sanic')

#function to clean and lemmatize comments
def clean_comments(text):
    #remove punctuations
    regex = re.compile('[' + re.escape(string.punctuation) + '\\r\\t\\n]')
    nopunct = regex.sub(" ", str(text))
    #use spacy to lemmatize comments
    lemmas=[]
    for i in range(0, len(nopunct), 100000):
        chunk = nopunct[i:i + 100]
        doc = nlp(chunk, disable=['parser','ner'])
        lemmas.extend([token.lemma_ for token in doc])
    return lemmas

def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

def words(text): return re.findall('[a-z]+', text.lower()) 

def setup_logging(log_level=logging.INFO):
	"""Set up the logging."""
	logging.basicConfig(level=log_level,filename=f'log/{datetime.now().ctime()}.log')
	fmt = ("%(asctime)s %(levelname)s "
		   "[%(name)s] %(message)s")
	colorfmt = "%(log_color)s{}%(reset)s".format(fmt)
	datefmt = '%Y-%m-%d %H:%M:%S'

	# Suppress overly verbose logs from libraries that aren't helpful
	logging.getLogger('requests').setLevel(logging.WARNING)
	logging.getLogger('urllib3').setLevel(logging.WARNING)
	logging.getLogger('aiohttp.access').setLevel(logging.WARNING)

	try:
		from colorlog import ColoredFormatter
		logging.getLogger().handlers[0].setFormatter(ColoredFormatter(
			colorfmt,
			datefmt=datefmt,
			reset=True,
			log_colors={
				'DEBUG': 'cyan',
				'INFO': 'green',
				'WARNING': 'yellow',
				'ERROR': 'red',
				'CRITICAL': 'red',
			}
		))
	except ImportError:
		pass

	logger = logging.getLogger('')
	logger.setLevel(log_level) 
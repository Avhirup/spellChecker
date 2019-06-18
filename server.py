from sanic import Sanic
from sanic.response import json
from sanic import response

from datetime import datetime
import logging
import traceback
import argparse

from utils import setup_logging
from checker.textblobchecker import TextBlobChecker
from checker.gingeritchecker import GingerItChecker
from checker.scratchchecker import ScratchChecker
from preprocess_rules import rule_pipe

app = Sanic(__name__)
_LOGGER = logging.getLogger('sanic')
argparser = argparse.ArgumentParser(description='Spelling Correction app')
argparser.add_argument('--checker', choices=["gingerit","textblob","scratch"], default="gingerit")
args = argparser.parse_args()

checker=GingerItChecker(rule_pipe)

if args.checker=='gingerit':
	checker=GingerItChecker(rule_pipe)
elif args.checker=='scratch':
	checker=ScratchChecker(rule_pipe)
else:
	checker=TextBlobChecker(rule_pipe)

@app.route("/spellCorrect",methods=['POST'])
async def post_handler(request):
	"""
	Method to execute at POST 
	Parameters
	----------
	request: sanic request object
		Request with sentence
	Returns
	-------
	response object
	"""
	try:
		result={}
		st_dt=datetime.now()
		word=request.json['word']
		result={"corrected_words":checker.checks_spell(word)}
		#get list of repositories based on stars	
		en_dt=datetime.now()
		_LOGGER.info(f"Time Taken {en_dt-st_dt}")
		
		return response.json(result,headers={'X-Served-By':'avhirup'},status=200)
	except KeyError as ke:
		return response.json({"message":f"Please provide:{ke}"},headers={'X-Served-By':'avhirup'},status=400)
	except Exception as e:
		print(traceback.print_stack())
		return response.json({"message":f"Something failed:{e}"},headers={'X-Served-By':'avhirup'},status=500)

@app.route("/repos",methods=['GET','PUT','DELETE','PATCH','OPTIONS','HEAD'])
async def other_handler(request):
	""" 
	Parameters
	----------
	request: sanic request object
		Request with org_id
	Returns
	-------
	response object
	"""
	return response.json({"message":f"Try POST instead"},headers={'X-Served-By':'avhirup'},status=405)

@app.route("/",methods=['GET'])
async def default(request):
	"""
	Redirect to use API ENDPOINT /repos instead
	Parameters
	----------
	request: sanic request object
	Returns
	-------
	response object
	"""
	return response.json({"message":f"Try API_ENDPOINT: /spellCorrect "},headers={'X-Served-By':'avhirup'},status=200)

if __name__ == '__main__':
	setup_logging()
	app.run(host="0.0.0.0", port=8080,workers=4)
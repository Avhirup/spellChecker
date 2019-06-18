# Rest API: Spell correction 
Following repository is a spell correction engine which takes in input word and returns list of corrected words.
## Features:
* Multiple SpellChecker Engines for spell correction:
    - Gingerit: Uses online API for spell correction.
    - TextBlob: Uses textblob downloded offline for spell correction.
    - Scratch: Custom spell checker built from scratch.
* Option for adding preprocessing rules:
    * Remove non alphanumeric.
    * Option to add custom rules. Custom make a child class with base class 'RULE' and override process function
* Handles Collocation:
    * Based on the provided text corpus and set threshold for frequency and PMI. Words like 'New York' as considered single word instead of 'New' and 'York'.
* Logging:
    - All server logs are saved in log folder.
* Async Request:
    * Able to process multiple requests asyncronously .Thanks to Sanic.

## Environment
python version : 3.6.8
* create environment
    * conda create -n haikujam python=3.6
* activate environment
    * source activate haikujam
* install required packages as mentioned in requirements.txt
    * pip install -r requirements.txt

## Usage:
### For Gingerit and Textblob:
    * Start server:
    PYTHONDONTWRITEBYTECODE=1 python server.py --checker='gingerit'
    * send request:
    -   curl  -X POST \
          http://127.0.0.1:8080/spellCorrect \
           -d '{
                "word":"helloworld"
        }'
    * {"corrected_words":["hello","world"]}
    * Note: gingerit fails at sometimes and may result in  "Empty reply from server error".Wait few mins and try again.This because of HTTPS and HTTP conflict or limit to API_KEY used in gingerit.

### For Custom corpus:
    * Build token frequency:
        * PYTHONDONTWRITEBYTECODE=1 python collocation_finder.py --corpus_path='text_corpus.txt'
    * Start server:
        * PYTHONDONTWRITEBYTECODE=1 python server.py --checker='scratch'
    * send request:
        * curl  -X POST \
          http://127.0.0.1:8080/spellCorrect \
           -d '{
                "word":"somethingold"
        }'
        * Validate response:{"corrected_words":["something","old"]}

# Examples:
* Multiple words joined together with spelling mistake:
    * curl  -X POST \
  http://127.0.0.1:8080/spellCorrect \
   -d '{
        "word":"samethingold"
    }'
    * Response:
    {"corrected_words":["something","old"]}
* Words with special character or smileys.
    * curl  -X POST \
      http://127.0.0.1:8080/spellCorrect \
       -d '{
            "word":"goodmarningÇ"
    }'
    * {"corrected_words":["good","morning"]}
* All ready correct words:
    * curl  -X POST \
  http://127.0.0.1:8080/spellCorrect \
   -d '{
        "word":"hell"
}'
    * {"corrected_words":["hell"]}
* Single word mispelled: 
    * curl  -X POST \
      http://127.0.0.1:8080/spellCorrect \
       -d '{
            "word":"nighty"
    }'
    * {"corrected_words":["night"]}
# To Do:
* In scratch engine:
    * The corpus used is small and the vocabulary is limited.For practical purposes we would need to choose dataset based on use case. For social media applications,https://www.english-corpora.org/tv/ is a good option as the language is informal and contains several slangs.
    * Google has released Web n-grams @ https://catalog.ldc.upenn.edu/LDC2006T13 . This contains many bigrams, trigrams , 4 grams & 5-grams with their correponding frequency.This could significantly increase detection of phrases with multiple words.

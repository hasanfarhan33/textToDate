import re
from datetime import date

import dateparser
import arrow

# IMPORTING NLTK
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# IMPORTING SPACY
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
nlp = spacy.load('en_core_web_md')

from colorama import Fore, Back, init, Style
init(autoreset=True)

texts = ["I will see you tomorrow.", "Day after tomorrow", "On 3rd January.", "First of December.", "We met last Sunday.",
         "Yesterday was a good day", "See you next Monday", "12th November, 1963"]

dateString = "Today is:\n24-11-2020\n24/11/2020\n24/11/20\n11/24/2020\n24 Nov 2020" \
             "\n24 November 2020\nNov 24, 2020\nNovember 24, 2020\n5-11-2020\n5/11/2020\n5/11/20\n11/5/2020" \
             "\n5 Nov 2020\n5 November 2020\nNov 5, 2020\nNovember 5, 2020\n24-9-2020\n24/9/2020" \
             "\n24/9/20\n9/24/2020\n24 Sep 2020\n24 September 2020\nSep 24, 2020\nSeptember 24, 2020" \
             "\n3-1-2020\n3/1/2020\n3/1/20\n1/3/2020\n3 Jan 2020\n3 January 2020\nJan 3, 2020" \
             "\nJanuary 3, 2020 "

months = {'01': 'January', '02': 'February', '03':'March', '04':'April', '05':'May', '06':'June', '07':'July', '08':'August', '09':'September',
          '10':'October', '11':'November', '12':'December'}

def extractionUsingRe(string: str):
    print(Fore.GREEN + Style.BRIGHT + "__USING RE__")
    print(Fore.GREEN + Style.DIM + "Extracting dates 'XX-XX-XXXX and XX/XX/XXXX':", re.findall(r'\d{2}[/-]\d{2}[/-]\d{4}', dateString)) # Extracting dates 'XX-XX-XXXX' and 'XX/XX/XXXX'
    print(Fore.GREEN + Style.DIM + "Extracting dates 'XX-XX-XX' and 'XX/XX/XX':", re.findall(r'\d{2}[/-]\d{2}[/-]\d{2,4}', dateString)) # Extracting dates 'XX-XX-XX' and 'XX/XX/XX'
    print(Fore.GREEN + Style.DIM + "Extracting 'X-X-XX' and 'X/X/XX':", re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', dateString)) # Extracting 'X-X-XX' and 'X/X/XX'
    print(Fore.GREEN + Style.DIM + "Extracting 3-spelled months:", re.findall(r'\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2,4}', dateString)) # Extracting 3-spelled months
    print(Fore.GREEN + Style.DIM + "Extracting fully written months:", re.findall(r'\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{2,4}', dateString)) # Extracting fully written months

def extractionUsingNltk(string:str):
    stringTokens = word_tokenize(string)

    # FILTERING STOP WORDS
    stop_words = set(stopwords.words("english"))
    stop_words.remove('after')
    filteredList = [word for word in stringTokens if word.casefold() not in stop_words]

    print(stringTokens)
    print(filteredList)

    # POS TAGGING
    print(nltk.pos_tag(filteredList))

def extractionUsingSpacy(string:str):
    stringDoc = nlp(string)
    stringTokens = [word.text for word in stringDoc]

    # FILTERING STOP WORDS
    filteredWords = []

    # Ignoring certain stop words
    nlp.vocab['after'].is_stop = False
    nlp.vocab['next'].is_stop = False
    nlp.vocab['last'].is_stop = False

    for word in stringTokens:
        lexeme = nlp.vocab[word]
        if lexeme.is_stop == False:
            filteredWords.append(word)

    print(stringTokens)
    print(filteredWords)

    # POS TAGGING
    # TODO: Try POS TAGGING

def extractionUsingArrowAndNltk(string: str):
    pass

# extractionUsingRe(dateString)
# extractionUsingNltk(texts[6])
# extractionUsingSpacy(texts[6])
extractionUsingArrowAndNltk(texts)
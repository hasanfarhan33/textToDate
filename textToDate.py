import re
from datetime import date

import dateparser
import arrow

# IMPORTING NLTK
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from colorama import Fore, Back, init, Style
init(autoreset=True)

texts = ["I will see you tomorrow.", "Day after tomorrow", "On 3rd January.", "First of December.", "We met last Sunday.",
         "Yesterday was a good day", "See you next Monday", "12th November, 1963", "a decade ago", "I bought it last week",
         "I bought this in March"]

dateString = "Today is:\n24-11-2020\n24/11/2020\n24/11/20\n11/24/2020\n24 Nov 2020" \
             "\n24 November 2020\nNov 24, 2020\nNovember 24, 2020\n5-11-2020\n5/11/2020\n5/11/20\n11/5/2020" \
             "\n5 Nov 2020\n5 November 2020\nNov 5, 2020\nNovember 5, 2020\n24-9-2020\n24/9/2020" \
             "\n24/9/20\n9/24/2020\n24 Sep 2020\n24 September 2020\nSep 24, 2020\nSeptember 24, 2020" \
             "\n3-1-2020\n3/1/2020\n3/1/20\n1/3/2020\n3 Jan 2020\n3 January 2020\nJan 3, 2020" \
             "\nJanuary 3, 2020 "

months = {'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6, 'july':7, 'august':8, 'september':9,
          'october':10, 'november':11, 'december':12}
weekdays = {0:'monday', 1:'tuesday', 2:'wednesday', 3:'thursday', 4:'friday', 5:'saturday', 6:'sunday'}

def extractionUsingRe(string: str):
    print(Fore.GREEN + Style.BRIGHT + "__USING RE__")
    print(Fore.GREEN + Style.DIM + "Extracting dates 'XX-XX-XXXX and XX/XX/XXXX':", re.findall(r'\d{2}[/-]\d{2}[/-]\d{4}', dateString)) # Extracting dates 'XX-XX-XXXX' and 'XX/XX/XXXX'
    print(Fore.GREEN + Style.DIM + "Extracting dates 'XX-XX-XX' and 'XX/XX/XX':", re.findall(r'\d{2}[/-]\d{2}[/-]\d{2,4}', dateString)) # Extracting dates 'XX-XX-XX' and 'XX/XX/XX'
    print(Fore.GREEN + Style.DIM + "Extracting 'X-X-XX' and 'X/X/XX':", re.findall(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', dateString)) # Extracting 'X-X-XX' and 'X/X/XX'
    print(Fore.GREEN + Style.DIM + "Extracting 3-spelled months:", re.findall(r'\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{2,4}', dateString)) # Extracting 3-spelled months
    print(Fore.GREEN + Style.DIM + "Extracting fully written months:", re.findall(r'\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{2,4}', dateString)) # Extracting fully written months
def filteringUselessWords(string:str) -> str:
    stringTokens = word_tokenize(string)
    stop_words = set(stopwords.words("english"))
    print("Stop Words: ", stop_words)
    stop_words.remove('after')
    stop_words.remove('before')
    stop_words.add('see')
    stop_words.add('day')
    stop_words.add('good')

    filteredList = [word for word in stringTokens if word.casefold() not in stop_words]

    posTaggedElements = nltk.pos_tag(filteredList)

    wordsToReturn = []
    for word, tag in posTaggedElements:
        if tag == "NN" or tag == "NNP" or tag == "IN" or tag == "CD" or tag == "JJ" or tag == "RB":
            wordsToReturn.append(word)

    # print(posTaggedElements)
    # print(filteredList)
    print("Filtering Results: ", wordsToReturn)

    return wordsToReturn

def extractionUsingArrowAndNltk(string: str):
    filteredWords = filteringUselessWords(string)

    # MANIPULATING DATES
    currentDate = arrow.now()

    if len(filteredWords) == 1:
        print(filteredWords)
        if filteredWords[0].lower() == 'tomorrow':
            resDate = currentDate.shift(days = -1).date()
        elif filteredWords[0].lower() == 'yesterday':
            resDate = currentDate.shift(days = 1).date()
        elif filteredWords[0].lower() in months:
            if currentDate.month > months[filteredWords[0].lower()]:
                resDate = currentDate.shift(months = -(currentDate.month - months[filteredWords[0].lower()])).date()
            elif months[filteredWords[0].lower()] > currentDate.month:
                resDate = currentDate.shift(months = (months[filteredWords[0].lower()] - currentDate.month)).date()
            # print(months[filteredWords[0].lower()])

    elif len(filteredWords) == 2:
        print(filteredWords)
    elif len(filteredWords) == 3:
        print(filteredWords)
    else:
        print("Something is wrong, you are an absolute failure and a waste of life")

extractionUsingArrowAndNltk(texts[9])
# filteringUselessWords(texts[9])

# WRITTEN STRINGS
# yesterday ---> days -= 1
# tomorrow ---> days += 1
# last __
# next __
# *num* __ ago
# __ ago
# day after tomorrow ---> days += 2
# day before yesterday ---> days -= 2
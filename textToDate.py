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

from word2number import w2n

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
weekdays = {'monday':0, 'tuesday':1, 'wednesday':2, 'thursday':3, 'friday':4, 'saturday':5, 'sunday':6}
daysTh = {'first':1, 'second':2, 'third':3, 'fourth':4, 'fifth':5, 'sixth':6, 'seventh':7, 'eighth':8, 'ninth':9, 'tenth':10, 'eleventh':11,
        'twelfth':12, 'thirteenth':13, 'fourteenth':14, 'fifteenth':15, 'sixteenth':16, 'seventeenth':17, 'eighteenth':18, 'ninteenth':19,
        'twentieth':20, 'twenty first':21, 'twenty second':22, 'twenty third':23, 'twenty fourth':24, 'twenty fifth': 25, 'twenty sixth':26,
        'twenty seventh':27, 'twenty eighth':28, 'twenty ninth':29, 'thirtieth':30, 'thirty first':31}

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
    # print("Stop Words: ", stop_words)
    stop_words.remove('after')
    stop_words.remove('before')
    stop_words.add('see')
    stop_words.add('day')
    stop_words.add('good')

    filteredList = [word for word in stringTokens if word.casefold() not in stop_words]

    wordsToReturn = []
    for word, tag in nltk.pos_tag(filteredList):
        if tag == "NN" or tag == "NNP" or tag == "IN" or tag == "CD" or tag == "JJ" or tag == "RB":
            wordsToReturn.append(word)

    posTaggedElements = nltk.pos_tag(wordsToReturn)
    print(posTaggedElements)
    # print(filteredList)
    print("Filtering Results: ", wordsToReturn)

    return wordsToReturn, list(posTaggedElements)

def fixingCardinalStrings(cardinalString: str):
    if not cardinalString[-1].isdigit() and cardinalString[0].isdigit():
        fixedString = ''
        for c in cardinalString:
            if c.isdigit():
                fixedString+=c
        return int(fixedString)
    else:
        return cardinalString

def extractionUsingArrowAndNltk(string: str):
    filteredWords, posTaggedElements = filteringUselessWords(string)

    # MANIPULATING DATES
    currentDate = arrow.now()

    if len(filteredWords) == 1:
        print(filteredWords)
        if filteredWords[0].lower() == 'tomorrow':
            resDate = currentDate.shift(days = -1).date()
            return resDate
        elif filteredWords[0].lower() == 'yesterday':
            resDate = currentDate.shift(days = 1).date()
            return resDate
        elif filteredWords[0].lower() in months:
            if currentDate.month > months[filteredWords[0].lower()]:
                resDate = currentDate.shift(months = -(currentDate.month - months[filteredWords[0].lower()])).date()
                return resDate
            elif months[filteredWords[0].lower()] > currentDate.month:
                resDate = currentDate.shift(months = (months[filteredWords[0].lower()] - currentDate.month)).date()
                return resDate
            # print(months[filteredWords[0].lower()])

    elif len(filteredWords) == 2:
        print(filteredWords)
        if filteredWords[0].lower() == 'last':
            # last week
            # print(currentDate.weekday())
            if filteredWords[-1].lower() == 'week':
                resDate = currentDate.shift(days = -7).date()
                return resDate
            # last month
            if filteredWords[-1].lower() == 'month':
                if currentDate.month == 1:
                    resDate = currentDate.shift(year = -1).date()
                    resDate = currentDate.replace(months = 12).date()
                    return resDate
                else:
                    resDate = currentDate.shift(months = -1).date()
                    return resDate
            # last year
            if filteredWords.lower() == 'year':
                resDate = currentDate.shift(years = -1).date()
                return resDate
            # last *weekday*
            #TODO: Test this crap (this seems a bit shady)
            if filteredWords.lower() in weekdays:
                resDate = currentDate.replace(weekday = -(weekdays[filteredWords[-1].lower()])).date()
                return resDate
        elif filteredWords[0].lower() == 'next':
            # next week
            if filteredWords[-1].lower() == 'week':
                resDate = currentDate.shift(days = 7).date()
                return resDate
            # next month
            if filteredWords[-1].lower() =='month':
                resDate = currentDate.shift(months = 1).date()
                return resDate
            # next year
            if filteredWords[-1].lower() == 'year':
                resDate = currentDate.shift(years = 1).date()
                return resDate
            # next *weekday*
            if filteredWords[-1].lower() in weekdays:
                resDate = currentDate.replace(weekday = weekdays[filteredWords[-1].lower()])
                return resDate

        elif filteredWords[-1].lower() == 'ago':
            # day ago (no one really says this but better safe than sorry)
            if filteredWords[0].lower() == 'day':
                resDate = currentDate.shift(days = -1)
                return resDate
            # week ago
            if filteredWords[0].lower() == 'week':
                resDate = currentDate.shift(days = -7)
                print(resDate)
            # month ago
            if filteredWords[0].lower() == 'month':
                if currentDate.month == 1:
                    resDate = currentDate.shift(years = -1, months = -1)
                    return resDate
                else:
                    resDate = currentDate.shift(months = -1)
                    return resDate
            # year ago
            if filteredWords[0].lower() == 'year':
                resDate = currentDate.shift(years= -1)
                return resDate

        # [3rd, January] [Third, January]
        elif filteredWords[-1].lower() in months:
            fixedString = fixingCardinalStrings(posTaggedElements[0][0])
            # [3rd, January]
            if type(fixedString) == int:
                resDate = currentDate.replace(days = fixedString, months = months[filteredWords[-1].lower()]).date()
            # [Third, January]
            else:
                if fixedString.lower() in daysTh:
                    resDate = currentDate.replace(days = daysTh[fixedString.lower()], months = months[filteredWords[-1].lower()]).date()
                else:
                    print("Something's wrong I can feel it!")

        # [November, 5th] [November, Fifth]
        elif filteredWords[0].lower() in months:
            fixedString = fixingCardinalStrings(posTaggedElements[0][-1])

            if type(fixedString) == int:
                resDate = currentDate.replace(days = fixedString, months = months[filteredWords[0].lower()]).date()
            else:
                if fixedString.lower() in daysTh:
                    resDate = currentDate.replace(days = daysTh[fixedString.lower()], months = months[filteredWords[0].lower()]).date()
                else:
                    print("Well this feeling I've got. Like something is about to happen. But I don't know what.")

        # Day after tomorrow
        elif filteredWords[-1].lower() == 'tomorrow' and filteredWords[0].lower() == 'after':
            resDate = currentDate.shift(days = 2)
        # Day before yesterday
        elif filteredWords[-1].lower() == 'yesterday' and filteredWords[0].lower() == 'before':
            resDate = currentDate.shift(days = -2)


    elif len(filteredWords) == 3:
        print(filteredWords)
        # *nums* days ago
        if filteredWords[1].lower() == 'days' and filteredWords[-1].lower() == 'ago':
            if filteredWords[0].isdigit():
                resDate = currentDate.shift(days=-int(filteredWords[0])).date()
            else:
                resDate = currentDate.shift(days = -int(w2n.word_to_num(filteredWords[0].lower()))).date()
        # *nums* months ago
        elif filteredWords[1].lower() == 'months' and filteredWords[-1].lower() == 'ago':
            if filteredWords[0].isdigit():
                resDate = currentDate.shift(months=-int(filteredWords[0])).date()
            else:
                resDate = currentDate.shift(months= -int(w2n.word_to_num(filteredWords[0].lower()))).date()
        # *nums* years ago
        elif filteredWords[1].lower() == 'years' and filteredWords[-1].lower() == 'ago':
            if filteredWords[0].isdigit():
                resDate = currentDate.shift(years=-int(filteredWords[0])).date()
            else:
                resDate = currentDate.shift(years = -int(w2n.word_to_num(filteredWords[0].lower()))).date()

    else:
        print("Something is wrong, you are an absolute failure and a waste of life. Here's a shovel, go dig your own grave.")

extractionUsingArrowAndNltk(texts[1])
# filteringUselessWords(texts[9])

# __STRING PATTERNS__
#   yesterday ---> days -= 1
#   tomorrow ---> days += 1
#   last __
#   next __
#   *num* __ ago
#   __ ago
#   day after tomorrow ---> days += 2
#   day before yesterday ---> days -= 2
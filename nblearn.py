#!/usr/bin/python
import sys
import os
import string
import json
import glob
if len(sys.argv) != 2: exit(0)
stopWords = { "a": None, "about": None, "above": None, "after": None, "again": None, "against": None, "all": None, "am": None, "an": None, "and": None, "any": None, "are": None, "aren't": None, "as": None, "at": None, "be": None, "because": None, "been": None, "before": None, "being": None, "below": None, "between": None, "both": None, "but": None, "by": None, "can't": None, "cannot": None, "could": None, "couldn't": None, "did": None, "didn't": None, "do": None, "does": None, "doesn't": None, "doing": None, "don't": None, "down": None, "during": None, "each": None, "few": None, "for": None, "from": None, "further": None, "had": None, "hadn't": None, "has": None, "hasn't": None, "have": None, "haven't": None, "having": None, "he": None, "he'd": None, "he'll": None, "he's": None, "her": None, "here": None, "here's": None, "hers": None, "herself": None, "him": None, "himself": None, "his": None, "how": None, "how's": None, "i": None, "i'd": None, "i'll": None, "i'm": None, "i've": None, "if": None, "in": None, "into": None, "is": None, "isn't": None, "it": None, "it's": None, "its": None, "itself": None, "let's": None, "me": None, "more": None, "most": None, "mustn't": None, "my": None, "myself": None, "no": None, "nor": None, "not": None, "of": None, "off": None, "on": None, "once": None, "only": None, "or": None, "other": None, "ought": None, "our": None, "ours": None, "ourselves": None, "out": None, "over": None, "own": None, "same": None, "shan't": None, "she": None, "she'd": None, "she'll": None, "she's": None, "should": None, "shouldn't": None, "so": None, "some": None, "such": None, "than": None, "that": None, "that's": None, "the": None, "their": None, "theirs": None, "them": None, "themselves": None, "then": None, "there": None, "there's": None, "these": None, "they": None, "they'd": None, "they'll": None, "they're": None, "they've": None, "this": None, "those": None, "through": None, "to": None, "too": None, "under": None, "until": None, "up": None, "very": None, "was": None, "wasn't": None, "we": None, "we'd": None, "we'll": None, "we're": None, "we've": None, "were": None, "weren't": None, "what": None, "what's": None, "when": None, "when's": None, "where": None, "where's": None, "which": None, "while": None, "who": None, "who's": None, "whom": None, "why": None, "why's": None, "with": None, "won't": None, "would": None, "wouldn't": None, "you": None, "you'd": None, "you'll": None, "you're": None, "you've": None, "your": None, "yours": None, "yourself": None, "yourselves":None}

def getPaths(path):
    CLASS = list()
    c = [os.path.join(path, x) for x in os.listdir(path)
            if os.path.isdir(path + '/' + x)]
    for i in range(len(c)):
        for x in [os.path.join(c[i], x) for x in os.listdir(c[i])
                if os.path.isdir(c[i]+'/' + x)]:
            CLASS.append(x)
    return CLASS

def labelMe(data):
    if 'positive' in data.lower() and 'truthful' in data.lower():
        return 'PT'
    if 'positive' in data.lower() and 'deceptive' in data.lower():
        return 'PD'
    if 'negative' in data.lower() and 'truthful' in data.lower():
        return 'NT'
    if 'negative' in data.lower() and 'deceptive' in data.lower():
        return 'ND'

def extractVocab(paths):
    V = dict()
    N = 0
    NC = dict()
    for path in paths:
        docs = glob.glob(path + '/*/*.txt')
        label = labelMe(path)
        NC[label] = len(docs)
        N = N + NC[label]

        for doc in docs:
            with open(doc, 'r') as f:
                data = f.read().strip().translate(None, string.punctuation)
                data = data.translate(None, '0123456789')
                data = data.lower().split()
                data = [x for x in data if not x in stopWords]
                for text in data:
                    V[text] = V.get(text, 0)
    return V, N, NC

def countTokenInClass(textC, path):
        result = 0
        docs = glob.glob(path + '/*/*.txt')
        for doc in docs:
            with open(doc, 'r') as f:
                data = f.read().strip().translate(None, string.punctuation)
                data = data.translate(None, '0123456789')
                data = data.lower().split()
                data = [x for x in data if not x in stopWords]
                for text in data:
                    result += 1
                    textC[text] = textC.get(text, 0) + 1
        return result

def train(paths):
    V, N, NC = extractVocab(paths)
    for path in paths:
        label = labelMe(path)
        prior = float(NC[label]) / N
        # Concatenate text of all docs from all classes in string
        textC = V.copy()
        # Count token of terms
        # Tct = Tokens that belong to this class
        Tct = countTokenInClass(textC, path)
        for text in textC:
            textC[text] = float(textC[text] + 1)/(Tct + len(V))
        #Update into the final database
        database[label] = (prior, textC)

database = {'PT' : {}, 'PD' : {}, 'NT' : {}, 'ND' : {}}
CLASSES = getPaths(sys.argv[1])
train(CLASSES)
json.dump(database,open('nbmodel.txt', 'w'))

#!/usr/bin/python
import glob
import math
import sys
import os
import json
import string

if len(sys.argv) != 2: exit(0)
testFiles = glob.glob(sys.argv[1] + '/*/*/*/*.txt')
database = json.load(open('nbmodel.txt', 'r'))
fname = 'nboutput.txt'
fhand = open(fname, 'w')
stopWords = {"a": None, "about": None, "above": None, "after": None, "again": None, "against": None, "all": None, "am": None, "an": None, "and": None, "any": None, "are": None, "aren't": None, "as": None, "at": None, "be": None, "because": None, "been": None, "before": None, "being": None, "below": None, "between": None, "both": None, "but": None, "by": None, "can't": None, "cannot": None, "could": None, "couldn't": None, "did": None, "didn't": None, "do": None, "does": None, "doesn't": None, "doing": None, "don't": None, "down": None, "during": None, "each": None, "few": None, "for": None, "from": None, "further": None, "had": None, "hadn't": None, "has": None, "hasn't": None, "have": None, "haven't": None, "having": None, "he": None, "he'd": None, "he'll": None, "he's": None, "her": None, "here": None, "here's": None, "hers": None, "herself": None, "him": None, "himself": None, "his": None, "how": None, "how's": None, "i": None, "i'd": None, "i'll": None, "i'm": None, "i've": None, "if": None, "in": None, "into": None, "is": None, "isn't": None, "it": None, "it's": None, "its": None, "itself": None, "let's": None, "me": None, "more": None, "most": None, "mustn't": None, "my": None, "myself": None, "no": None, "nor": None, "not": None, "of": None, "off": None, "on": None, "once": None, "only": None, "or": None, "other": None, "ought": None, "our": None, "ours": None, "ourselves": None, "out": None, "over": None, "own": None, "same": None, "shan't": None, "she": None, "she'd": None, "she'll": None, "she's": None, "should": None, "shouldn't": None, "so": None, "some": None, "such": None, "than": None, "that": None, "that's": None, "the": None, "their": None, "theirs": None, "them": None, "themselves": None, "then": None, "there": None, "there's": None, "these": None, "they": None, "they'd": None, "they'll": None, "they're": None, "they've": None, "this": None, "those": None, "through": None, "to": None, "too": None, "under": None, "until": None, "up": None, "very": None, "was": None, "wasn't": None, "we": None, "we'd": None, "we'll": None, "we're": None, "we've": None, "were": None, "weren't": None, "what": None, "what's": None, "when": None, "when's": None, "where": None, "where's": None, "which": None, "while": None, "who": None, "who's": None, "whom": None, "why": None, "why's": None, "with": None, "won't": None, "would": None, "wouldn't": None, "you": None, "you'd": None, "you'll": None, "you're": None, "you've": None, "your": None, "yours": None, "yourself": None, "yourselves":None}

C = {'PT': 'truthful positive', 'PD' : 'deceptive positive',
'NT': 'truthful negative', 'ND': 'deceptive negative'}

def applyMultinomialNB(fhand, docs):
    for doc in docs:
        with open(doc, 'r') as f:
            words = f.read().strip().translate(None, string.punctuation)
            words = words.translate(None, '0123456789')
            words = words.lower().split()
            words = [x for x in words if not x in stopWords]
            score = dict()
            for c in C.keys():
                score[c] = math.log(database[c][0])
                for word in words:
                    try:
                        score[c] += math.log(database[c][1][word])
                    except KeyError:
                        pass

            maxKey, maxValue = None, None
            for key, value in score.items():
                if maxValue == None or value > maxValue:
                    maxKey = key
                    maxValue = value
            fhand.write(C[maxKey] + ' ' + doc + '\n')

    fhand.close()

applyMultinomialNB(fhand, testFiles)
fhand.close()

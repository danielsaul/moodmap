import logging, re
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize, sent_tokenize, wordpunct_tokenize

logger = logging.getLogger('moodmap.sentiment.bayes')

url_matcher = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
at_matcher = re.compile(r"([@])(\w+)\b")
emoticons_regex = r"(?:[<>]?[:;=8xX][\-o\*\']?[\)\]\(\[dDpPsS/\:\}\{@\|\\]|[\)\]\(\[dDpPsS/\:\}\{@\|\\][\-o\*\']?[:;=8xX][<>]?)"
emo_matcher = re.compile(emoticons_regex)
token_matcher = re.compile(r"(" + emoticons_regex + "|(?:[a-zA-Z][a-zA-Z'\-_]+[a-zA-Z])|(?:[+\-]?\d+[,/.:-]\d+[+\-]?)|(?:[\w_]+)|(?:\.(?:\s*\.){1,})|(?:\S))")
neg_matcher = re.compile(r"(?:^(?:never|no|nothing|nowhere|noone|none|not|havent|hasnt|hadnt|cant|couldnt|shouldnt|wont|wouldnt|dont|doesnt|didnt|isnt|arent|aint)$)|n't")
clause_matcher = re.compile(r"^[.,:;!?]$")
punc_matcher = re.compile(r"[^\w\s]")

class Tokeniser():
    def __init__(self, tweet):
        self.tweet = tweet
        self.tokenise()

    def tokenise(self):
        tweet = unicode(self.tweet)
        tweet = tweet.replace("#", "") # Get rid of the # in hashtags
        tweet = url_matcher.sub("", tweet) # Remove URLs
        tweet = at_matcher.sub("", tweet) # Remove @usernames
        tokens = token_matcher.findall(tweet)
        self.tokens = map((lambda x : x if emo_matcher.search(x) else x.lower()), tokens)
        return self.tokens

    def remove_noise(self):
        return

    def handle_negation(self):
        negated = False
        for i, token in enumerate(self.tokens):
            if clause_matcher.search(token) != None:
                negated = False
            elif negated:
                self.tokens[i] = "not_" + token
                negated = False
            elif neg_matcher.search(token) != None:
                negated = True
        return self.tokens

    def remove_punctuation(self):
        return filter((lambda x : not (punc_matcher.match(x) is not None and len(x) == 1)), self.tokens)

import sys
import json

def hw():
    print 'Hello, world!'

def lines(fp):
    print str(len(fp.readlines()))

def buildSentimentDict(sent_file):
    afinnfile = open(sent_file)
    scores = {}
    # initialize an empty dictionary
    for line in afinnfile:
        term, score = line.split("\t") # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score) # Convert the score to an integer.
    return scores

def getSentiment(sent_dict, tweet):
    affin = 0.0
    if "text" in tweet:
        for word in tweet["text"].split(" "):
            #print "Searching for %s in sent_dict" % word
            if word in sent_dict:
                affin += sent_dict[word]
    return affin

def main():
    sent_dict = buildSentimentDict(sys.argv[1])
    tweet_file = open(sys.argv[2])
    for tweet in tweet_file:
        json_tweet = json.loads(tweet)
        affin = getSentiment(sent_dict, json_tweet)
        print affin

if __name__ == '__main__':
    main()

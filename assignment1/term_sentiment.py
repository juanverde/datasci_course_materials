import sys
import json

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
        for word in tweet["text"].split(" "): #print "Searching for %s in sent_dict" % word
            if word in sent_dict:
                affin += sent_dict[word]
    return affin

positive_term_sent = {}
negative_term_sent = {}

def tabulateTerms(sent_dict, tweet, affin):
    if not "text" in tweet:
        return
    for word in tweet["text"].split(" "):
        if not word in sent_dict:
            if affin > 0:
                if not word in positive_term_sent:
                    positive_term_sent[word] = 0.0
                positive_term_sent[word] += 1.0
            if affin < 0:
                if not word in negative_term_sent:
                    negative_term_sent[word] = 0.0
                negative_term_sent[word] += 1.0

def getTermAffinity(term):
    affin = 0.0
    pos_count = 0
    neg_count = 0

    if term in positive_term_sent:
        pos_count = positive_term_sent[term]

    if term in negative_term_sent:
        neg_count = negative_term_sent[term]                

    if pos_count > 0 and neg_count > 0:
        if pos_count > neg_count:
            affin = pos_count / neg_count
        elif neg_count > pos_count:
            affin = -1 * ( neg_count / pos_count)
    elif pos_count > 0:
        affin = pos_count
    elif neg_count > 0:
        affin = -1 * neg_count

    return affin

def main():
    sent_dict = buildSentimentDict(sys.argv[1])
    tweet_file = open(sys.argv[2])
    for tweet in tweet_file:
        try:
            json_tweet = json.loads(tweet)
            affin = getSentiment(sent_dict, json_tweet)
            tabulateTerms(sent_dict, json_tweet, affin)
        except Exception:
            pass
           
    all_terms = set(positive_term_sent.keys())
    all_terms = all_terms.union(negative_term_sent.keys())
    for term in all_terms:
        term_affin = getTermAffinity(term)
        print "%s %f" % (term, term_affin)
 

if __name__ == '__main__':
    main()

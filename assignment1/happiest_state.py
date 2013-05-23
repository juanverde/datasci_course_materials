import sys
import json
import re

state_regex = '.*?[, ](A[KLRZ]|C[AOT]|D[EC]|FL|GA|HI|I[ADLN]|K[SY]|LA|M[ADEINOST]|N[CDEHJMVY]|O[HKR]|PA|RI|S[CD]|T[NX]|UT|V[AT]|W[AIVY]).*'
state_affin = {}

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

def getStateFromField(field):
    state = ''

    m = re.match(state_regex, field, flags=re.IGNORECASE)
    if not None == m:
        state = m.group(1).upper()

    return state

def getStateFromTweet(tweet):
    state = ''
    if "place" in tweet and not tweet["place"] == None:
        place = tweet["place"]
        if "full_name" in place and not place["full_name"] == None:
            full_name = place["full_name"]
            state = getStateFromField(full_name)

    if not state == '' and "user" in tweet and not tweet["user"] == None:
        user = tweet["user"]
        if "location" in user and not user["location"] == None:
            location = user["location"]
            state = getStateFromField(location)

    return state

def main():
    sent_dict = buildSentimentDict(sys.argv[1])
    tweet_file = open(sys.argv[2])
    for tweet in tweet_file:
        try:
            json_tweet = json.loads(tweet)
            state = getStateFromTweet(json_tweet)
            if not '' == state:
                affin = getSentiment(sent_dict, json_tweet)
                if not state in state_affin:
                    state_affin[state] = 0.0
                state_affin[state] += affin
        except Exception, ex:
            pass

    max_affin = -99999
    happiest_state = ""
    for state in state_affin:
        if state_affin[state] > max_affin:
            happiest_state = state
            max_affin = state_affin[state]

    print happiest_state

if __name__ == '__main__':
    main()

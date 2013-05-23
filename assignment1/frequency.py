import sys
import json

term_counts = {}

def countTerms(tweet):
    term_count = 0.0
    if "text" in tweet:
        for word in tweet["text"].split(" "): #print "Searching for %s in sent_dict" % word
            if not word in term_counts:
                term_counts[word] = 0.0
            term_counts[word] += 1.0
            term_count += 1.0
    return term_count
            

def main():
    tweet_file = open(sys.argv[1])
    total_count = 0.0
    for tweet in tweet_file:
        try:
            json_tweet = json.loads(tweet)
            count = countTerms(json_tweet)
            total_count += count
        except Exception:
            pass
           
    for term in term_counts:
        print "%s %f" % (term.replace("\n", ""), term_counts[term] / total_count)
 

if __name__ == '__main__':
    main()

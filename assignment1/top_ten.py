import sys
import json
import heapq
from functools import total_ordering

@total_ordering
class HashtagCount:
    def __init__(self, hashtag):
        self._hashtag = hashtag.strip()
        self._count = 0.0

    def incr(self):
        self._count += 1.0

    def getHashtag(sef):
        return self._hashtag

    def getCount(self):
        return self._count

    def __lt__(self, other):
        retval = False
        if hasattr(other, '_count'):
            retval = self._count < other._count
        return retval

    def __eq__(self, other):
        retval = False
        if hasattr(other, '_hashtag'):
            retval = self._hashtag == other._hashtag
        return retval

    def __str__(self):
        return "%s %f" % (self._hashtag, self._count)

hashtag_counts = {}

def addHashtagsToCounts(tweet):
    if "entities" in tweet:
        entities = tweet["entities"]
        if "hashtags" in entities:
            #print entities["hashtags"]
            for hashtag in  entities["hashtags"]: 
                hashtag_text = hashtag["text"]
                if not hashtag_text in hashtag_counts:
                    hashtag_counts[hashtag_text] = HashtagCount(hashtag_text)
                hashtag_counts[hashtag_text].incr()
           

def main():
    tweet_file = open(sys.argv[1])
    for tweet in tweet_file:
        try:
            json_tweet = json.loads(tweet)
            addHashtagsToCounts(json_tweet)
        except Exception:
            pass

    ordering = []
    for hashtag_count in hashtag_counts.values():
        heapq.heappush(ordering, hashtag_count)

    for hashtag_count in heapq.nlargest(10, ordering):
        print hashtag_count


if __name__ == '__main__':
    main()

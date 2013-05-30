import MapReduce
import sys

"""
Identify any asymetric friendships in a social network
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # key: person
    # value: friend
    key = record[0]
    value = record[1]
    mr.emit_intermediate(key, record)
    mr.emit_intermediate(value, record)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    #print "key is %s" % key
    friend_of_me = set()
    my_friends = set()
    for v in list_of_values:
      person = v[0]
      friend = v[1]
      if not person == key:
        friend_of_me.add(person)
      if not friend == key:
        my_friends.add(friend)
    #print my_friends
    #print friend_of_me

    asym_friends = my_friends - friend_of_me

    #print asym_friends

    for a in asym_friends:
      mr.emit((key, a))

    asym_people = friend_of_me - my_friends 
    #print asym_people
    for a in asym_people:
      mr.emit((key, a))


# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

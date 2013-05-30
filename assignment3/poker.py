import MapReduce
import sys

"""
Calculate occurences of poker hands
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

# Python Mapper() : Given unique 5-card hand (csv string), return the made hand.
# e.g. 'flush', 'straight', etc  
def mapper(record):
  cards = record.split(',')  # 5 cards like 'QH' (for Q of hearts) 

  # Get counts of all faces and suits. 
  counts = ({ 
      '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0, 'T':0, 
      'J':0, 'Q':0, 'K':0, 'A':0, 
      'S':0, 'C':0, 'D':0, 'H':0 
    }) 
  for card in cards: 
    face = card[0] 
    suit = card[1] 
    counts[face] += 1 
    counts[suit] += 1 

  is_flush = ( 
      (counts['S'] == 5) or 
      (counts['C'] == 5) or 
      (counts['D'] == 5) or 
      (counts['H'] == 5)) 

  is_straight = False 
  straightrunfaces = 'A23456789TJQKA';  # note: ace ('A') appears twice
  for i in range(0, 10): 
    if (counts[straightrunfaces[i]] and 
        counts[straightrunfaces[i+1]] and 
        counts[straightrunfaces[i+2]] and 
        counts[straightrunfaces[i+3]] and 
        counts[straightrunfaces[i+4]]): 
      is_straight = True 
      break 

  is_4card_straight = False 
  for i in range(0, 11): 
    if (counts[straightrunfaces[i]] and 
        counts[straightrunfaces[i+1]] and 
        counts[straightrunfaces[i+2]] and 
        counts[straightrunfaces[i+3]]): 
      is_4card_straight = True 
      break 


  is_quad, is_trip, is_pair, is_two_pair = False, False, False, False 
  faces = 'A23456789TJQK' 
  for i in range(0, len(faces)): 
    face_count = counts[faces[i]] 
    if face_count == 4: 
      is_quad = True 
    elif face_count == 3: 
      is_trip = True 
    elif face_count == 2: 
      if is_pair:  # saw another pair before? 
        is_two_pair = True 
      is_pair = True 
 
  # Emit output: a (stringized) count of '1' for the detected hand.
  if is_straight and is_flush: 
    mr.emit_intermediate('straightflush', '1') 
  elif is_quad: 
    mr.emit_intermediate('4ofakind', '1') 
  elif is_trip and is_pair: 
    mr.emit_intermediate('fullhouse', '1') 
  elif is_flush: 
    mr.emit_intermediate('flush', '1') 
  elif is_straight: 
    mr.emit_intermediate('straight', '1') 
  elif is_4card_straight: 
    mr.emit_intermediate('4cardstraight', '1') 
  elif is_trip: 
    mr.emit_intermediate('3ofakind', '1') 
  elif is_two_pair: 
    mr.emit_intermediate('2pair', '1') 
  elif is_pair: 
    mr.emit_intermediate('pair', '1') 
  else: 
    mr.emit_intermediate('highcard', '1') 


# Python Reducer() : key is a made hand, e.g. 'flush' .
# Count up how many unique hands make e.g. a flush.
def reducer(key, list_of_values):
  sum = 0; 
  for v in list_of_values:
    count_str = v
    count = int(count_str) # convert to int for summing 
    sum += count 

  output_str = '%s:%d' % (key, sum) 
  mr.emit(output_str) 

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

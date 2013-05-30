import MapReduce
import sys

"""
Multiply two matracies using MapReduce
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

size = 5

def mapper(record):
    # record: source matrix, row, column, value
    matrix = record[0]
    row = record[1]
    col = record[2]
    if matrix == 'a':
      for i in xrange(size):
        mr.emit_intermediate((row, i), record)
    elif matrix == 'b':
      for i in xrange(size):
        mr.emit_intermediate((i, col), record)

def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    row = None
    col = None
    value = 0

    rows = {}
    cols = {}

    for val in list_of_values:
      if val[0] == 'a':
        if row == None:
          row = val[1]

        rows[val[2]] = val

      elif val[0] == 'b':
        if col == None:
          col = val[2]

        cols[val[1]] = val

    if row == None or col == None:
      return

    for i in xrange(size):
      if i in rows and i in cols:
        value += rows[i][3] * cols[i][3]
      
    mr.emit((row, col, value))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

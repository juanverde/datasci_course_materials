import MapReduce
import sys

"""
Implement a SQL join with Map Reduce
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    # The second field of both the order and line item records are the order_id
    mr.emit_intermediate(record[1], record)

def reducer(key, list_of_values):
    order = None
    for v in list_of_values:
      if v[0] == 'order':
        order = v
        break

    if order == None:
      return

    for v in list_of_values:
      if v[0] == 'line_item':
        mr.emit(order + v)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)

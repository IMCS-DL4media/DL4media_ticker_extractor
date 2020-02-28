import csv

"""
Commonly used functions for operating with TSV files
"""

def read(path):
  """
  Returns list of dictionaries.
  
  All returned values will be strings.
  Will assume that first row of file contains column names.
  """
  
  file = open(path, 'r', encoding = 'utf-8')
  reader = csv.reader(file, delimiter = '\t', quotechar = '', quoting = csv.QUOTE_NONE)
  result = []
  header = reader.__next__()
  for values in reader:
    entry = {}
    for i in range(len(header)):
      entry[header[i]] = values[i]
    result.append(entry)
  file.close()
  return result
  
def write(l, path, columns):
  """
  Writes write list of dictionaries to Tab Seperated Value file.
  
  Will make everything a string.
  Will make first row dictionary names.
  Only the "columns" fields of dictionaries will be written.
  
  Throws KeyError exception if dictionary doesn't contain a key from 
  "columns".
  """
  
  file = open(path, 'w', newline = '', encoding = 'utf-8')
  writer = csv.writer(file, delimiter = '\t', quotechar = '', quoting = csv.QUOTE_NONE)
  row = []
  for col in columns:
    row.append(col)
  writer.writerow(row)
  for entry in l:
    row = []
    for col in columns:
      row.append(entry[col])
    writer.writerow(row)
  file.close()
import os

def makedirs(path):
  """
  Makes directories, and doesn't raise error when they already exist.
  """
  
  if not os.path.exists(path):
    os.makedirs(path)
    
def cleandir(path):
  """
  Deletes all files in a folder.
  """
  
  for file in os.listdir(path):
    os.remove(path + '/' + file)

def inrange(val, minval, maxval):
    return (val >= minval) & (val <= maxval)

def requests(method, kwargs):
  if method in kwargs and kwargs[method] == True:
    return True
  else:
    return False
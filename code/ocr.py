class OCR():
  """Baseclass for things that accept images and return lists of words.
  
  This abstraction exists because I wanted it to be easy to swap out different
  OCR engines.
  """
  
  def __init__(self):
    self._images = []
    
  def __del__(self):
    del self._images
  
  def _preprocess(self, image):
    """
    Adjusts the image so that OCR can better read it.
    """
    
    return image.copy()
  
  def _preprocess_list(self, images):
    return [self._preprocess(img) for img in images]
  
  def add(self, images):
    """
    Preprocesses and adds images to list for next read.

    images - numpy array or list of numpy arrays corresponding to image/s.
    """
  
    if not type(images) is list:
      images = [images]
    self._images = self._images + self._preprocess_list(images)
  
  def _runocr(self, images):
    """
    Takes preprocessed image list, runs OCR, and returns texts.
    """
    raise NotImplementedError
  
  def read(self, images = None, language = None):
    """
    Takes image/s reads them and returns a list of lists of words.
    
    By word here I mean a dictionary with fields:
      'text';
      'left', 'top', 'right', 'bottom' - position of word in image;
      'confidence' - 0..1 how certain the OCR engineis that it read correctly.
    
    images - numpy array or list of numpy arrays corresponding to image/s.
      Defaults to queue of images added by "add" function.
    """
    
    if images is None:
      images = self._images
      self._images = []
    else:
      if not type(images) is list:
        images = [images]
      images = self._preprocess_list(images)
    if len(images) == 0:
      return []
    else:
      return self._runocr(images, language)
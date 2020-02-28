import cv2
import numpy as np

def frames_to_float(frames):
    return (frames / 255).astype(np.float32)

def frames_to_int(frames):
    return (frames * 255).astype(np.uint8)

def frames_threshold(frames, minv = 0.0, maxv = 1.0):
    return np.maximum(np.minimum(frames, maxv), minv)

def frames_gray(frames):
    return frames.mean(axis = 2)

def frames_blur_rectangle(frames, shape = [5, 5]):
    kernel = np.ones(shape, dtype = np.float32) / (shape[0] * shape[1])
    return cv2.filter2D(frames, -1, kernel)

def gamma_to_intensity(frames, gamma = 2.2, **kwargs):
    """
    Transforms numbers to represent intensities of light rather than rgb
    values.
    """
    
    return np.power(frames, 1 / gamma)

def gamma_to_rgb(frames, gamma = 2.2, **kwargs):
    """
    Transforms intensities of light back to rgb values.
    """
    
    return np.power(frames, gamma)

def hist_adjust_new_method(frames, dark_new = 0.1, bright_new = 0.9, **kwargs):
    """
    Divides image into dark and bright part.
    Calculates average of dark part and average of bright part.
    Does linear transformation so that
      The average dark part value would correspond to "dark_new" and
      The average bright part value would correspond to "bright_new".
    Truncates values to [0..1]
    
    frames - numpy array.
    """
    
    avg = frames.mean()

    dark_map = frames < avg
    bright_map = ~ dark_map
    dark_avg = frames[dark_map].mean()
    bright_avg = frames[bright_map].mean()

    delta = bright_avg - dark_avg
    frames = (frames - dark_avg) / delta * (bright_new - dark_new) + dark_new

    frames = np.maximum(0, frames)
    frames = np.minimum(1, frames)
    
    return frames

def hist_adjust(frames, method = 'newone', **kwargs):
  """
  General method for calling brightness, contrast or histogram changing 
  preprocessing.
  
  method - 'newone' for method described in paper, or None for no method.
  gamma_correct - If set to True, preprocessing is done with intensity values
    instead of mean rgb values.
  """
  
  #Turn to grayscale
  frames = frames.mean(-1)
  
  if method is None:
    pass
  elif method == 'newone':
    return hist_adjust_new_method(frames, **kwargs)
  else:
    raise ValueError('Method "' + str(method) + '" unknown.')

  return frames
  
def resize_font(frame, height, new_height = 32, interpolation = 'cubic', **kwargs):
    """
    Resize the image to have a new font height.
    
    frame - numpy array of image.
    height - current font height in pixels of capital letter.
    new_height - desired font height.
    interpolation - method of interpolation accepts:
        'nearest', 'linear' and 'cubic'
    """
    
    scale_factor = new_height / height
    new_size_x = (int) (frame.shape[1] * scale_factor)
    new_size_y = (int) (frame.shape[0] * scale_factor)
    
    if interpolation == 'cubic':
        interpolation = cv2.INTER_CUBIC
    elif interpolation == 'linear':
        interpolation = cv2.INTER_LINEAR
    elif interpolation == 'nearest':
        interpolation = cv2.INTER_NEAREST
    else:
        raise ValueError('Interpolation method "' + str(interpolation) + '" not implemented.')
        
    frame = cv2.resize(frame, (new_size_x, new_size_y), interpolation = interpolation)
    
    frame = np.maximum(0, frame)
    frame = np.minimum(1, frame)
    
    return frame
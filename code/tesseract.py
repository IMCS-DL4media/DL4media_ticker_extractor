import cv2

import subprocess

from ocr  import OCR
import tsv
from utils import makedirs, cleandir, requests
from frameops import *

class TesseractOCR(OCR):
  """OCR that uses Tesseract OCR
  """
  
  def __init__(self, tmp_path = './ocr/TesseractOCR/tmp', **preprocesses):
    super(TesseractOCR, self).__init__();
    self.tmp_path = tmp_path
    self._preprocesses = preprocesses
    makedirs(tmp_path + '/input')
    makedirs(tmp_path + '/output')
  
  def _preprocess(self, image):
    if requests('gamma_correct', self._preprocesses):
      image = gamma_to_intensity(image, **self._preprocesses)
  
    image = hist_adjust(image, **self._preprocesses)
    
    if requests('resize_font', self._preprocesses):
      if 'height' in self._preprocesses:
        image = resize_font(image, **self._preprocesses)
        #As the deadline comes closer, the entropy of this code increases exponentially
        if 'new_height' in self._preprocesses:
          new_height = self._preprocesses['new_height']
        else:
          new_height = 32
        self.scale_factor = new_height / self._preprocesses['height']
      else:
        raise Error('Tried to calculate height')
        image = resize_font(image, height = image.shape[0], **self._preprocesses)
    else:
      self.scale_factor = 1.0
        
    if requests('add_padding', self._preprocesses):
      if 'padding' in self._preprocesses:
        pad = self._preprocesses['padding']
      else:
        pad = 2
      
      edges = np.concatenate([image[:2], image[-2:]], axis = 0)
      if edges[edges < edges.mean() + 0.001].size > edges[edges > edges.mean() - 0.001].size:
        pad_color = edges[edges < edges.mean() + 0.001].mean()
      else:
        pad_color = edges[edges > edges.mean() - 0.001].mean()
      
      image = np.pad(image, ((pad, pad), (0, 0)), mode = 'constant', constant_values = pad_color)
        
    if requests('gamma_correct', self._preprocesses):
      image = gamma_to_rgb(image, **self._preprocesses)
  
        
    return image
  
  def _runocr(self, images, language = None):
    image_list_path = self.tmp_path + '/input' + '/image_list.txt'
    image_list = open(image_list_path, 'w')
    for img_num in range(len(images)):
      name = str(img_num) + '.png'
      image_path = self.tmp_path + '/input' + '/' + name
      images[img_num] = frames_to_int(images[img_num])
      #Write images to disk
      cv2.imwrite(image_path, images[img_num])
      #Write image names to disk
      image_list.write(image_path + '\n')
    image_list.close()
    
    if language is None or language == 'English':
      lan = 'eng'
    elif language == 'Latvian':
      lan = 'lav2'
    elif language == 'Russian':
      lan = 'rus'
    else:
      raise ValueError('Language ' + language + ' not implemented')
    output_path = self.tmp_path + '/output' + '/words'
    #Run OCR and write read words to Tab Seperated Value file
    subprocess.call(['tesseract', image_list_path, output_path, '-l', lan, '--psm', '6', 'tsv'])
    #Read it as list of dict
    ocr_output = tsv.read(output_path + '.tsv')
    
    #Format output to more usable form.
    result = []
    for row in ocr_output:
      #Check if new image started
      if row['level'] == '1':
        last_page = row['page_num']
        result.append([])
      #Check if row is a word
      elif (row['level'] == '5') and\
           (len(row['text']) > 0) and\
           (row['text'] != ' '):
        word = {}
        word['text'] = row['text']
        word['left'] = float(row['left']) / self.scale_factor
        word['top'] = float(row['top']) / self.scale_factor
        word['right'] = (float(row['left']) + float(row['width'])) / self.scale_factor
        word['bottom'] = (float(row['top']) + float(row['height'])) / self.scale_factor
        word['confidence'] = float(row['conf']) / 100.0
        result[-1].append(word)
    
    #Clean tmp
    cleandir(self.tmp_path + '/input');
    cleandir(self.tmp_path + '/output');
    return result
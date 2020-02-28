import cv2
import numpy as np

import math

from frameops import *

h = 0
w = 0

#Currently return only one ticker
def get_tickers(video, sample_count = 200):
    samples = [(int) (i / sample_count * (video.frame_count - 1)) for i in range(sample_count)]
    #Calculate average absolute change in brigtness
    difference_sum = np.zeros(video.shape[:2], dtype = np.float32)
    for frame_num in samples:
        frame1 = video.frame(frame_num)
        frame2 = video.frame()
        difference_sum+= frames_gray(abs(frame1 - frame2))
    difference_sum/= sample_count
    
    difference_blur = difference_sum #frames_blur_rectangle(difference_sum, [5, 5])
    threshold = np.amax(difference_blur) * 0.9
    success, text_pixels = cv2.threshold(difference_blur, threshold, 1.0, cv2.THRESH_BINARY)
    
    #Check every pixel
    minx = 1000000
    maxx = -1
    miny = 1000000
    maxy = -1
    for y in range(video.height):
        for x in range(video.width):
            if text_pixels[y, x] > 0.5:
                minx = min(minx, x)
                maxx = max(maxx, x)
                miny = min(miny, y)
                maxy = max(maxy, y)
    
    #Expand text box one line at a time, as long as the next line is texty enough.
    expand_threshold = threshold * 0.5
    expand_threshold_up = threshold * 0.15
    while True:
        expanded = False
        
        #Edge check
        if minx == 0:
            pass
        elif difference_blur[miny:maxy+1, minx-1:minx].mean() > expand_threshold:
            minx-= 1
            expanded = True
        
        if maxx == video.width - 1:
            pass
        elif difference_blur[miny:maxy+1, maxx+1:maxx+2].mean() > expand_threshold:
            maxx+= 1
            expanded = True
            
        if miny == 0:
            pass
        elif difference_blur[miny-1:miny, minx:maxx+1].mean() > expand_threshold_up:
            miny-= 1
            expanded = True
        
        if maxy == video.height - 1:
            pass
        elif difference_blur[maxy+1:maxy+2, minx:maxx+1].mean() > expand_threshold:
            maxy+= 1
            expanded = True
        
        if not expanded:
            break
    
    global h
    global w
    
    h = maxy - miny + 1
    w = maxx - minx + 1
    
    #Correct for blur
    #minx-= 2;
    #maxx+= 2;
    #miny-= 2;
    #maxy+= 2;
    
    #Add space for diacritics;
    miny-= math.floor(h * 1/3 + 1)
    maxy+= math.floor(h * 1/3 + 1)
    
    tickers = np.array([[[miny, maxy], [minx, maxx]]], dtype = np.int32)
    #Check for video borders
    tickers = np.maximum(tickers, 0)
    tickers = np.minimum(tickers, np.array([[[video.height - 1], [video.width - 1]]], dtype = np.int32))
        
    
    return tickers

def get_tickers_hw(video, sample_count = 200):
  return (get_tickers(video, sample_count), h, w)
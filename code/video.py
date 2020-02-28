import cv2

from frameops import *

class Video():
    def __init__(self, path, ocr = None, language = None):
        video = cv2.VideoCapture(path)
        
        self.video_capture = video
        
        self.frame_rate = video.get(cv2.CAP_PROP_FPS)
        self.frame_duration = 1 / self.frame_rate
        self.frame_count = self._get_frame_count()
        self.height = (int) (video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.width = (int) (video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.shape = [self.height, self.width, 3]
        if language is not None:
            self.language = language
        elif ocr is not None:
            self.language = self._guess_language(ocr)
        else:
            self.language = None
    
    def __del__(self):
        del self.video_capture
    
    #CV2 function for this is not reliable
    def _get_frame_count(self):
        def got_frame(video):
            success, frm = video.read()
            return success
        
        frame_count = 0
        while got_frame(self.video_capture):
            frame_count+= 1
        self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        return frame_count
    
    def frame(self, frame_number = None):
        if frame_number is not None:
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        read_success, image = self.video_capture.read()
        image = frames_to_float(image)
        return image
        
    def _test_language(self, language, frame_numbers, ocr):
        frames = [self.frame(frame_number) for frame_number in frame_numbers]
        output = ocr.read(frames, language = language)
        confidence = 0
        for word_list in output:
          for word in word_list:
              confidence+= word['confidence'] * len(word['text'])
        return confidence
        
    def _guess_language(self, ocr):
        #Simply tests for which language ocr reads the most stuff
    
        #Sample test frames
        """sample_count = 20
        if self.frame_count < sample_count:
            frame_numbers = [i for i in range(self.frame_count)]
        else:
            step = self.frame_count // sample_count
            frame_numbers = [i * step for i in range(sample_count)]
    
        languages = ['Latvian', 'English', 'Russian']
        max_confidence = - 1
        max_language = None
        for language in languages:
            confidence = self._test_language(language, frame_numbers, ocr)
            if confidence > max_confidence:
              max_confidence = confidence
              max_language = language
        """
        return 'Latvian'
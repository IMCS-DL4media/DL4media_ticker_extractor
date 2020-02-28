from slidingreader import read_tickers
from storyops import concatenate_news_stories
from video import Video

import sys, getopt

def cl_help():
  print('Usage: easyrun.py -o outputfile.txt inputfile.mp4')

try:
  options, args = getopt.getopt(sys.argv[1:], 'ho:')
except getopt.GetoptError:
  cl_help()
  sys.exit(2)

if len(args) != 1:
  cl_help()
  sys.exit(2)

input_name = args[0]
output_name = 'output.txt'

for option, arg in options:
  if option == '-h':
    cl_help()
    sys.exit()
  elif option == '-o':
    output_name = arg


best_parameters = {
    'jump_size': 12,
    'resize_font': True,
    'height': None,
    'new_height': 32,
    'interpolation': 'cubic',
    'add_padding': False,
    'method': None,
    'gamma_correct': True,
    'merge_method': 'confidence',
    'garbage_method': 'char_confidence',
    'garbage_threshold': 0.85,
    'overlap_method': 'merges'
}

video = Video(input_name, language = 'Latvian')
output = concatenate_news_stories(read_tickers(video, **best_parameters)[0], char = ' ')
f = open(output_name, 'w', encoding = 'utf8')
f.write(output)
f.close()
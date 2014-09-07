#!/usr/local/bin/python

import sys
import os
from audio_parse import *

parse_data = file('sample_data.txt', 'w')

for f in os.listdir('audio/sample')[1:]:
	x = audio_parse('audio/sample/' + f)
	parse_data.write(str(x) + '\n')

parse_data.close()
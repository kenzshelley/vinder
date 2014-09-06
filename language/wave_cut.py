import wave as w
import math

# This is a parameter controlling how long you want each chunk
SEGMENT_TIME = 6

def cut_wave(file_name):
	# Splits the wave file, but then returns a list of the new file names
	basename = file_name.split('/')[-1].replace('.wav', '')
	sounds = w.open(file_name, 'r')

	source_param = sounds.getparams()

	tot_frames = source_param[3]
	speed_frames = source_param[2]
	small_time = math.floor(0.6 * speed_frames)

	segments = tot_frames/(6 * speed_frames) + 1
	# print tot_frames
	# print speed_frames
	# print segments

	new_files = []
	cut = 0
	while sounds.tell() + speed_frames * SEGMENT_TIME < tot_frames + small_time:

		# Rewind a little bit so you're not in the middle of a word
		if cut > 0:	
			sounds.setpos(sounds.tell() - small_time)
		sound_chunk = sounds.readframes(speed_frames * SEGMENT_TIME)

		# Store the new name
		new_name = 'temp/' + basename + str(cut) + '.wav'
		new_files.append(new_name)

		# Now write a bit	
		sound_write = w.open(new_name, 'wb')
		sound_write.setparams(source_param)
		sound_write.setframerate(speed_frames * 0.8)
		sound_write.writeframes(sound_chunk)
		sound_write.close()

		cut = cut + 1

	# Now for the remaining chunk
	
	sounds.setpos(sounds.tell() - small_time)
	sound_chunk = sounds.readframes(tot_frames - int(sounds.tell()))

	new_name = 'temp/' + basename + str(cut) + '.wav'
	new_files.append(new_name)

	sound_write = w.open(new_name, 'wb')
	sound_write.setparams(source_param)
	sound_write.writeframes(sound_chunk)
	sound_write.close()

	return new_files

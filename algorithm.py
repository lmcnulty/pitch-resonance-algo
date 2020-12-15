import os
import subprocess
from statistics import median, mean
from time import time

datadir = './data'

normalize = lambda value, min, max: (value - min) / (max - min);

def plus_time(p, t):
	p[0] += t
	return p

pitch_data = []
formant_data = []
starttime = time()
currenttime = starttime
filecount = 0
cliplength = 1
for filename in os.listdir(datadir):
	filecount += 1
	data = subprocess.check_output(
		["praat", "--run", "backend.praat", datadir + '/' + filename], 
		universal_newlines=True
	)

	sections = data.split("## Pitch ##\n");
	if (len(sections) < 2):
		print("Could not parse Praat output:\n\n" + data)
	
	pitch_data += [
		plus_time([float(n) for n in line.split("\t") if n != ""], cliplength*filecount)
		for line in sections[1].split("\n") 
		if not "undefined" in line and len(line.split("\t")) > 1
	]
	formant_data += [
		plus_time([float(n) for n in line.split("\t") if n != ""], cliplength*filecount)
		for line in sections[0].split("\n")[1:-1]
		if not "undefined" in line and len(line.split("\t")) > 1
	]

	currenttime = time()
	t = currenttime - starttime
	
	radius = .5
	formant_selection = []
	pitch_selection = []
	while len(formant_selection) < 2 or len(pitch_selection) < 2:
		radius *= 2
		formant_selection = [p for p in formant_data if abs(t - p[0]) < radius]
		pitch_selection = [p for p in pitch_data if abs(t - p[0]) < radius]
		if radius > 4:
			print("Time: ", t)
			print("Radius: ", radius)
			print("Pitchdata: ", pitch_data)
			print("pitch_selection: ", pitch_selection)
			exit()
			break

	prenormalized_resonance = 	(
		.5 * normalize(mean([p[1] for p in formant_selection]), 100, 1000) +
		.5 * normalize(mean([p[2] for p in formant_selection]), 1100, 2000)
	)

	resonance = normalize(prenormalized_resonance, .2, .8)
	pitch = normalize(median([p[1] for p in pitch_selection]), 50, 300)

	print(filecount, t, pitch, resonance)

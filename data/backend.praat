form File
	sentence filename
endform

Read from file... 'filename$'
soundID = selected("Sound")

To Formant (burg)... 0.01 5 5000 0.025 50
List... no yes 6 no 3 no 3 no

appendInfoLine: "## Pitch ##"

select 'soundID'
To Pitch: 0, 75, 600
numFrames = Get number of frames
for i from 1 to numFrames
    time = Get time from frame number: i
    pitch = Get value at time... time Hertz Linear
    appendInfoLine: "'time'	'pitch'"
endfor


exit

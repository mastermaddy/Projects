import json
import os
import wave
import pyglet
from watson_developer_cloud import TextToSpeechV1

def exit_callback(dt):
    pyglet.app.exit()


def textToSpeech(s):
	text_to_speech = TextToSpeechV1(
	  username= "cd6d0299-40d7-4d77-b131-05beb7de172b",
	  password= "0b6iVnKvtuuy",
	    x_watson_learning_opt_out=True)  # Optional flag

	audio_file= open('C:\\Users\\dell\\Desktop\\Watson\\test1.wav','wb')#('/mnt/c/Users/dell/Desktop/Watson/test1.wav','wb') 
	audio_file.write(text_to_speech.synthesize( s[0], accept='audio/wav',voice="en-US_AllisonVoice"))
	audio_file.write(text_to_speech.synthesize( s[1], accept='audio/wav',voice="en-US_AllisonVoice"))
	audio_file.write(text_to_speech.synthesize( s[2], accept='audio/wav',voice="en-US_AllisonVoice"))
	audio_file.write(text_to_speech.synthesize( s[3], accept='audio/wav',voice="en-US_AllisonVoice"))
	audio_file.write(text_to_speech.synthesize( s[4], accept='audio/wav',voice="en-US_AllisonVoice"))


	for i in range(5,len(s)):
		audio_file.write(text_to_speech.synthesize( s[i], accept='audio/wav',voice="en-US_AllisonVoice"))		

	sound = pyglet.media.load('C:\\Users\\dell\\Desktop\\Watson\\test1.wav', streaming=False)
	sound.play()

	pyglet.clock.schedule_once(exit_callback , sound.duration)
	pyglet.app.run()
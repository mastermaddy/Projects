import imageRecognitionModule
import textToSpeechModule
import scrapModule
import os

scrapModule.getUrl()
fname=os.listdir('C:\\Users\\dell\\Downloads')
dirpath='C:\\Users\\dell\\Downloads'
fname.pop(0)
#print(fname)
fname.sort(key=lambda p: os.stat(dirpath+'\\'+p).st_mtime, reverse=True)
print(fname)
s=imageRecognitionModule.imageRecognition(dirpath+'\\'+fname[0])
textToSpeechModule.textToSpeech(s)



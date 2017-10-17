from lxml import html 
import requests
import os
import json
import urllib.request
from PIL import Image
from selenium.webdriver.common.keys import Keys
from pynput.keyboard import Key, Controller
#i1=page.find('\x22')
#i2=page.find('\x22',i1+4)

#print (i1)
#print (i2)

#length=i2-i1


#for x in range(i1,i2):
#	print (page[x])

#print (page)

from selenium import webdriver

def getUrl():

	f=open('credentials.json').read()
	d=json.loads(f)

	user=d['username']
	password=d['password']


	
	driver = webdriver.Chrome('C:\\Users\\dell\\Downloads\\downloads2\\chromedriver_win321\\chromedriver.exe')
	#Firefox('C:\\Users\\dell\\Downloads\\geckodriverwin64\\geckodriver.exe')
	#Chrome('C:\\Users\\dell\\Downloads\\chromedriver_win321\\chromedriver.exe')  
	driver.implicitly_wait(1)
	driver.get('https://drive.google.com/drive/folders/1uoGS5zrym2EE5hepWQdAKT5tTg')

	driver.find_element_by_css_selector('#Email').send_keys(user)
	driver.find_element_by_css_selector('#next').click()
	driver.find_element_by_css_selector('#Passwd').send_keys(password)
	driver.find_element_by_css_selector('#signIn').click()
	#driver.find_element_by_css_selector('#signIn').click()

	pgidL=[]
	while(len(pgidL)==0):
		html1 = driver.page_source
		page=(html1.encode('utf-8'))
		tree=html.fromstring(page)
		pgidL=tree.xpath('//div[@class="a-u-xb-j a-Wa-ka"]/@id')

	pgid=pgidL[0]	

	index=pgid.find('.')
	pgid=pgid[index+1:(len(pgid))]

	pgid='https://drive.google.com/open?id='+pgid


	oldname=os.listdir('C:\\Users\\dell\\Downloads')[0]

	driver.get(pgid)
	
	keyboard = Controller()
	keyboard.press(Key.ctrl)
	keyboard.press('s')
	keyboard.release(Key.ctrl)
	keyboard.release('s')
	keyboard.press(Key.enter)
	keyboard.release(Key.enter)
	#driver.find_element_by_css_selector('drive-viewer-icon drive-viewer-custom-button-icon drive-viewer-download-icon').click()

	
	#newname=os.listdir('C:\\Users\\dell\\Downloads')[0]

	


	for i in range (1,5):		
		driver.refresh()	




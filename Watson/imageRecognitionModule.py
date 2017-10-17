import json
from watson_developer_cloud import VisualRecognitionV3

def imageRecognition(fname):

	#test_url = url#'https://images.pexels.com/photos/104827/cat-pet-animal-domestic-104827.jpeg?w=940&h=650&auto=compress&cs=tinysrgb'

	visual_recognition = VisualRecognitionV3('2017-03-12', api_key="2982ddcd5b37096bf612b7b639b7f931605e474d")

	image_file= open(fname, 'rb')
	dict=json.loads(json.dumps(visual_recognition.classify(images_file=image_file, threshold=0.1,classifier_ids=['CarsvsTrucks_1479118188','default']), indent=2))



	#print(dict)

	keyList=dict['images'][0]['classifiers'][0]['classes']

	type_hierarchy_value=''
		
	x=keyList[1]

	classAttributes=[]

	for x in keyList:
		for pair in x:
			if pair=='type_hierarchy': 
				if len(x['type_hierarchy']) > len(type_hierarchy_value):
					type_hierarchy_value=x['type_hierarchy']
			if pair!='score' and pair!='type_hierarchy':		
				classAttributes.append(x[pair])

	classAttributes=list(set(classAttributes))


	thingsToprint=[]

	objcolor=''

	for x in classAttributes:
		if(type_hierarchy_value.find(x)==-1):
			if(x.find('color')==-1):
				thingsToprint.append(x)
			else:
				objcolor+=(', '+x)	


	#print (thingsToprint)
	#print (type_hierarchy_value)		
	#print (objcolor)


	properties='- '

	for x in thingsToprint:
		properties+=(x+', ')

	properties=properties[0:len(properties)-2]	

	type_hierarchy_value=type_hierarchy_value.replace('/','  ',10000)


	s1="The object has " + objcolor 
	s2="The object has following other properties " + properties 
	s3="The object has the following class hirarrchy - "+type_hierarchy_value

#	print(s1)
#	print(s2)
#	print(s3)

	s= [s1,s2,s3]

	with open(fname, 'rb') as image1_file:
		textD=json.loads(json.dumps(visual_recognition.recognize_text(images_file=image1_file),indent=2))

	myText=textD['images'][0]['text']
	  
	myText.replace('\n',' ',10000)

	if(len(myText)==0):
		s4='No text was found on the image'
	else:
		s4='The text found on the image is - '+(myText)

	s.append(s4)

	#print(s4)


	with open(fname, 'rb') as image_file:
		faceDict=json.loads(json.dumps(visual_recognition.detect_faces(images_file=image_file),indent=2))

	faceList=faceDict["images"][0]['faces']

	minAge=[]
	maxAge=[]
	gender=[]

	for face in faceList:
		minAge.append(face['age']['min'])
		maxAge.append(face['age']['max'])
		gender.append(face['gender']['gender'])

	if len(faceList)==0:
		Fstr='No  faces were detected in the image '

	elif len(faceList)==1:
		Fstr='The face detected in the image '

	else:
		Fstr='The faces detected in the image '		

	s.append(Fstr)
	Fstr=''
	for i in range(0,len(gender)):
		Fstr+=('\n' +'Face '+str(i+1)+'\n' 'Age between ')
		Fstr+=str(minAge[i])
		Fstr+=' to '
		Fstr+=str(maxAge[i])
		Fstr+=' and gender '
		Fstr+=gender[i]
		s.append(Fstr)
		Fstr=''
		

	print(Fstr)	

	#s.append(Fstr)

	return (s)

#imageRecognition('C:\\Users\\dell\\Downloads\\IMG_3425.JPG')	







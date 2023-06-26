from flask import Flask,render_template,redirect,url_for,request

from flask import request, render_template, url_for
from keras import models
import numpy as np
from PIL import Image
import string
import random
import os
app=Flask(__name__)
model = models.load_model('static/model/model.h5')

@app.route("/", methods=["GET", "POST"])
def index():
	normal='normal.png'
	a='a.png'
	s='s.png'
	l='l.png'

	# Execute if request is get
	if request.method == "GET":
		full_filename =  'R.png'
		return render_template("index.html", full_filename = full_filename,a=a,s=s,l=l,normal=normal)

	# Execute if reuqest is post
	if request.method == "POST":

		# Generating unique image name
		

		# Reading, resizing, saving and preprocessing image for predicition 
		
		letters = string.ascii_lowercase
		name = ''.join(random.choice(letters) for i in range(10)) + '.png'
		full_filename =  'static/' + name
		
		image_upload = request.files['image_upload']
	   
		imagename = image_upload.filename
		image = Image.open(image_upload).convert('RGB')
		image = image.resize((150,150))
		image.save(full_filename)
		image_arr = np.array(image.convert('RGB'))/255
		image_arr.shape = (1,150,150,3)
        
		# Predicting output
		result = model.predict(image_arr)
		ind = np.argmax(result)
		classes = ['adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib',
 'large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa' ,'normal',
 'squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa']

		# Returning template, filename, extracted text
		return render_template('index.html',full_filename=name, pred = classes[ind],a=a,s=s,l=l,normal=normal)

if __name__=='__main__':
    app.run(debug=True)



'''FROM TERMINAL
. CatApiApp/bin/activate
cd CatApiApp
export FLASK_ENV=development
export FLASK_APP=server.py
flask run
'''
from flask import Flask, render_template, url_for, jsonify
from bs4 import BeautifulSoup
import requests
from PIL import Image
import io 

#_name__ is our main 
app = Flask(__name__)

with open('templates/index.html') as fp:
	soup = BeautifulSoup(fp, 'html.parser')
	cat_button = soup.find(id = 'cat_button')
	cat_result = soup.find(id = 'cat_results')

	
#rendering the HTML page
@app.route('/')
def index_html():
	cat_result = generate_random_cats()

	'''TEST AREA
	res_img = requests.get(cat_result)
	img_bytes = io.BytesIO(res_img.content)
	img = Image.open(img_bytes)
	img.show()

	print('cats: ' + cat_result)
	print('----------------')
	'''
	return render_template('index.html', data = cat_result)

#generating random cat images on buttom click
@app.route('/randomcats')
def generate_random_cats():

	url = 'https://api.thecatapi.com/v1/images/search'
	payload = {}
	headers = {
	  '50427698-0fc1-4f8e-b67c-4b6fd9925152': ''
	}

	response = requests.request('GET', url, headers = headers, data = payload)

	if response.status_code != 200:
		raise RuntimeError(f'Error fetching: {response.status_code}, check the api and try again')
		return response
	else:
		if response == []:
			generate_random_cats()
		else:
			data = response.json()
			image_url = data[0]['url']

	#print('generate_random_cats(): ' + data[0]['url'])
	return data[0]['url']
	
if __name__ == '__main__':
	app.run()


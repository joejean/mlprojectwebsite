from flask import Flask, render_template, make_response, request, redirect, g, url_for, flash, session, jsonify
from app import app, dataset
from forms import passwordForm, categoriesForm, storesForm
from config import PASSWORD
from rq import Queue
from rq.job import Job
from worker import conn
from recommender import custom_recommend
import time




#function to validate a list of form instances
def form_validated_on_submit(forms):
	validated = False
	for form in forms:
		if form.validate_on_submit():
			validated = True
		else:
			validated = False

	return validated



@app.route('/', methods=['POST', 'GET'])
def login():
	form = passwordForm()
	if form.validate_on_submit():
		if form.password.data == PASSWORD:
			session['logged_in'] = True
			return redirect(url_for('home'))
		else:
			flash(u"Incorect Password", 'error')
			return render_template('login.html', form = form)
	return render_template("login.html", form = form)


@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	return redirect(url_for('login'))


@app.route('/recommender', methods=['POST', 'GET'])
def home():
	if session.has_key('logged_in'):
		data = [(u'footwear', u'footwear'),(u'fasion wholesale', u'fasion wholesale'),\
		(u'guest services', u'guest services'),(u'eyewear', u'eyewear'),\
		(u'books and digital media', u'books and digital media'),(u"women's shoes", u"women's shoes"),\
		(u"women's clothing", u"women's clothing"),(u'makeup', u'makeup'),(u"children's footwear", u"children's footwear"),\
		(u'diamonds', u'diamonds'),(u'skincare', u'skincare'),(u'cellular accessories', u'cellular accessories'),\
		(u"women's jewelry", u"women's jewelry"),(u'clothing & shoes', u'clothing & shoes'),(u'sporting goods', u'sporting goods'),\
		(u'chocolates', u'chocolates'),(u'personalized gifts', u'personalized gifts'),(u'shoes', u'shoes'),\
		(u"men's gifts", u"men's gifts"),(u'stuffed animals', u'stuffed animals'),(u'headwear', u'headwear'),\
		(u"children's apparel", u"children's apparel"),(u'clothing', u'clothing'),(u'consumer electronics', u'consumer electronics'),\
		(u'candles', u'candles'),(u'sports apparel', u'sports apparel'),(u'home furnishings', u'home furnishings'),\
		(u'furniture', u'furniture'),(u'video games', u'video games'),(u'sports clothing', u'sports clothing'),\
		(u"men's clothing", u"men's clothing"),(u"children's clothing", u"children's clothing"),(u'cookies', u'cookies'),\
		(u'restaurant', u'restaurant'),(u'nutritional supplements', u'nutritional supplements'),(u'denim', u'denim'),\
		(u'beauty products', u'beauty products'),(u' beauty products', u' beauty products'),(u'disney', u'disney'),\
		(u"women's handbags", u"women's handbags"),(u'plus size clothing', u'plus size clothing'),(u'telecommunication', u'telecommunication'),\
		(u'coffee', u'coffee'),(u'jewelry', u'jewelry'),(u'hair care', u'hair care'),(u' accessories', u' accessories'),\
		(u"girl's clothing", u"girl's clothing"),(u'department store', u'department store'),(u'maternity clothing', u'maternity clothing'),\
		(u'ice cream', u'ice cream'),(u' clothing', u' clothing'),(u'photography', u'photography'),(u'mattress', u'mattress'),\
		(u'perfume', u'perfume')]
		data.sort()
		form = categoriesForm()
		form.category.choices = data
		if request.method == 'POST' and form.validate_on_submit():
			session["selectedCategories"] = form.category.data
			return redirect(url_for('storesNumber'))
		else:
			return render_template('home.html', form = form)

	else:
		return redirect(url_for('login'))

@app.route('/storesNumber', methods = ['POST', 'GET'])
def storesNumber():
	if session["selectedCategories"]:
		catList = session["selectedCategories"]
		forms = []
		for cat in catList:
			forms.append(storesForm(prefix=cat))

		forms_with_categories = [(cat, form) for cat, form in zip(catList, forms)]


		if form_validated_on_submit(forms):
			#Dictionary that will be sent to the recommender in the following format
			#{'FirstMall': {'Men\'s Clothing':8, 'Beauty Products':11, 'Consumer Electronics':11}}
			dictionary = {"USERMALL":{}}

			#List of tuples that contains (cat, numberOfStores)
			list_ot_tuples = []

			for cat_form in forms_with_categories:
				list_ot_tuples.append((cat_form[0],cat_form[1].numberOfStores.data))

			dictionary["USERMALL"] = dict(list_ot_tuples)

			data = dataset.dict
			data.update(dictionary)

			#use a background process to run the recommender
			q = Queue(connection=conn)

			job = q.enqueue_call(func = custom_recommend, args=(data, "USERMALL"))
			#print custom_recommend(data,"USERMALL")

			return render_template('results.html', jobkey = job.get_id() )

		else:
			return render_template('stores_number.html', catList = catList, form = forms_with_categories );

	return redirect(url_for('home'))




@app.route('/getresults/<jobkey>', methods = ['GET'])
def getresults(jobkey):
	job = Job.fetch(jobkey, connection = conn)

	if (job.is_finished):
		return jsonify(job.result)
	else:
		return jsonify({"error":"error"}), 202


@app.route('/dataset')
def queryDataset():
	return render_template('dataset.html')

@app.route('/getstores/<mallname>', methods=['GET','POST'])
def getStores(mallname):

	malldata = {"name":"MallX",
					"stores":["JoeMall", "MaryMall", "ReneMall", "AntoineMall"]}
	if mallname == malldata['name']:

		return jsonify(malldata)

	return jsonify({})

	# return redirect(url_for('queryDataset'))



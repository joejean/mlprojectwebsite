from flask import Flask, render_template, make_response, request, redirect, g, url_for, flash, session, jsonify
from app import app, recommender
from forms import passwordForm, categoriesForm, storesForm
from config import PASSWORD

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
		data = [("Womens's Clothing","Women's Clothing" ), ("Men's Clothing", "Men's Clothing"), ('Consumer Electronics','Consumer Electronics')]
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
			#Dictionary that will be sent to the recommender in the follwoing format
			#{'FirstMall': {'Men\'s Clothing':8, 'Beauty Products':11, 'Consumer Electronics':11}}
			dictionary = {"XMALL":{}}

			#List of tuples that contains (cat, numberOfStores)
			list_ot_tuples = []

			for cat_form in forms_with_categories:
				list_ot_tuples.append((cat_form[0],cat_form[1].numberOfStores.data))

			dictionary["XMALL"] = dict(list_ot_tuples)

			recommender.dataset.update(dictionary)
			
			recommendations = recommender.custom_recommender(recommender.dataset,"XMALL")

			#Remove any previous recommendations that might have already been in session['recommendations'] 
			if (session.get('recommendations') != None):
				session.pop('recommendations')

			if recommendations:
				session['recommendations'] = recommendations
			# redirect(url_for('results'))

			return redirect(url_for('results'))

		else:
			return render_template('stores_number.html', catList = catList, form = forms_with_categories );

	return redirect(url_for('home'))


@app.route('/results')
def results():
	recommendations = session.get('recommendations')
	if (recommendations != None):
		return render_template("results.html", recommendations = recommendations)

	return render_template("results.html")




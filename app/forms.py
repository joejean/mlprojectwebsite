from flask.ext.wtf import Form
from wtforms.fields import PasswordField, BooleanField, IntegerField, SelectMultipleField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired
from wtforms import widgets

class passwordForm(Form):
	password = PasswordField('password', [DataRequired(message="Please enter a password")])



class categoriesForm(Form):
	category = SelectMultipleField('category',[DataRequired(message="Please select at least one category")],
	option_widget=widgets.CheckboxInput(),
    widget=widgets.ListWidget(prefix_label=False))

	
class storesForm(Form):
	numberOfStores = IntegerField('number_of_stores')


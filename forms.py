from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, validators
from wtforms.fields.html5 import DateField


class SignupForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=50)])
    last_name = StringField('Last Name', [validators.Length(min=1, max=50)])
    email_id = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    usertype = SelectField('User Type', choices=[('customer','Customer'), ('chef','Chef')])
    apartment_no = StringField('Apartment No', [validators.Length(min=1, max=50)])
    street = StringField('Street', [validators.Length(min=1, max=50)])
    city = StringField('City', [validators.Length(min=1, max=50)])
    state = StringField('State', [validators.Length(min=2, max=10)])
    zipcode = StringField('Zipcode', [validators.Length(min=4, max=10)])
    country = StringField('Country', [validators.Length(min=2, max=50)])
    phone_number = StringField('Phone', [validators.Length(min=4, max=50)])
    # cuisine = SelectField('Cuisine', choices=[(x['cuisineid'],x['cuisine_name']) for x in get_chefspecial()], coerce=int)
# END SignupForm


class OrderPageForm(Form):
    cuisineName = StringField('cuisine', [validators.Length(min=1, max=25)])
    orderDate = StringField('datepicker')
    comments = StringField('comments', [validators.Length(min=1, max=50)])
# END OrderPageForm


class DashboardOrderForm(Form):
    order_name = StringField('What\'s your order', [validators.Length(min=1, max=50)])
    requested_date = DateField('Requested date', format='%m/%d/%Y')
    comments = TextAreaField('Comments', [validators.Length(min=0)])
# END DashboardOrderForm

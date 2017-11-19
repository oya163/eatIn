from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, validators
from wtforms.fields.html5 import DateField

class SignupForm(Form):
    first_name = StringField('First Name *', [
        validators.Length(min = 1, max = 50),
        validators.DataRequired()
    ])

    last_name = StringField('Last Name *', [
        validators.Length(min = 1, max = 50),
        validators.DataRequired()
    ])

    email_id = StringField('Email *', [
        validators.Length(min = 6, max = 50),
        validators.DataRequired()
    ])

    password = PasswordField('Password *', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message = ' Passwords do not match')
    ])

    confirm = PasswordField('Confirm Password *', [
        validators.DataRequired()
    ])

    usertype = SelectField('User Type',
        choices = [('customer','Customer'), ('chef','Chef')]
    )

    # address information is optional
    apartment_no = StringField('Apartment No', [validators.Length(max = 50)])
    street = StringField('Street', [validators.Length(max = 50)])
    city = StringField('City', [validators.Length(max = 50)])
    state = StringField('State', [validators.Length(max = 10)])
    zipcode = StringField('Zipcode', [validators.Length(max = 10)])

    # build list of countries for selection
    country = SelectField('Country', coerce = int)

    # optional
    phone_number = StringField('Phone', [validators.Length(max=50)])
    # cuisine = SelectField('Cuisine', choices=[(x['cuisineid'],x['cuisine_name']) for x in get_chefspecial()], coerce=int)
# END SignupForm


class OrderPageForm(Form):
    cuisine = SelectField('Cuisine', coerce = int)


    orderDate = StringField('datepicker')
    comments = StringField('comments', [validators.Length(min=1, max=50)])
# END OrderPageForm


class ConfirmOrderForm(Form):
    requested_date = DateField('Requested Date', format='%Y-%m-%d')
    comment = TextAreaField('Comments', [validators.Length(min=0)])
# END ConfirmOrderForm


class FindMealForm(Form):
    cuisine = SelectField('Cuisine', coerce = int)
# END FindMealForm


class DashboardOrderForm(Form):
    cuisine = SelectField('Pick a Cuisine', coerce = int)
    #requested_date = DateField('Requested date', format='%m/%d/%Y')
    #comments = TextAreaField('Comments', [validators.Length(min=0)])
# END DashboardOrderForm

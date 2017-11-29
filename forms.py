import datetime

from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, validators
from wtforms_components import DateRange
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
        choices = [('customer','Customer'), ('chef','Chef'), ('both', 'Customer + Chef')]
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


class AccountForm(Form):
    # General options
    first_name = StringField('First Name * ', [
        validators.Length(min = 1, max = 50),
        validators.DataRequired()
    ])

    last_name = StringField('Last Name * ', [
        validators.Length(min = 1, max = 50),
        validators.DataRequired()
    ])

    email_id = StringField('Email * ', [
        validators.Length(min = 6, max = 50),
        validators.DataRequired()
    ])

    password = PasswordField('Password', [
        validators.EqualTo('confirm', message = ' Passwords do not match')
    ])

    confirm = PasswordField('Confirm Password', [
    ])

    usertype = SelectField('User Type',
        choices = [('customer','Customer'), ('chef','Chef'), ('both', 'Customer + Chef')]
    )

    apartment_no = StringField('Apartment No', [validators.Length(max = 50)])
    street = StringField('Street', [validators.Length(max = 50)])
    city = StringField('City', [validators.Length(max = 50)])
    state = StringField('State', [validators.Length(max = 10)])
    zipcode = StringField('Zipcode', [validators.Length(max = 10)])
    country = SelectField('Country', coerce = int)
    phone_number = StringField('Phone', [validators.Length(max=50)])

    # Chef options
    chefspec = SelectField('Chef Speciality Cuisine', coerce = int)
    reachouts = TextAreaField('Reachout Areas', [validators.Length(max = 500)])

    # Customer options
    custpref = StringField('Customer Preference Notes', [validators.Length(max=500)])
# END AccountForm


class OrderPageForm(Form):
    cuisine = SelectField('Cuisine', coerce = int)


    orderDate = StringField('datepicker')
    comments = StringField('comments', [validators.Length(min=1, max=50)])
# END OrderPageForm


class ConfirmOrderForm(Form):
    requested_date = DateField('Requested Date', format = '%Y-%m-%d',
                               validators=[DateRange(min = datetime.date.today())])
    comment = TextAreaField('Comments', [validators.Length(min = 0)])
# END ConfirmOrderForm


class FindMealForm(Form):
    cuisine = SelectField('Cuisine', coerce = int)
# END FindMealForm


class FindFoodForm(Form):
    cuisine = SelectField('Pick a Cuisine', coerce = int)
# END DashboardOrderForm


class FindChefForm(Form):
    country = SelectField('Pick a Country', coerce = int)
# END DashboardOrderForm

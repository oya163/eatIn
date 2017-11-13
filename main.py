import math
import random
import sys

from flask import Flask, session, redirect, g, url_for, escape, request, render_template, flash, logging, abort

from functools import wraps
from passlib.hash import sha256_crypt
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, validators
from wtforms.fields.html5 import DateField

import models

# app/db config stuff
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://<user>:<pass>@localhost/eatin'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')


# Index
@app.route('/')
def index():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html', session_user_name = username_session)
    return redirect(url_for('login'))


# Login
@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form fields
        email = request.form['username']
        passsword_candidate = request.form['password']

        user = Models.get_user_by_email(email)

        if user != None:
            # Compare passwords
            if sha256_crypt.verify(password_candidate, user.password):
                # Passed
                session['logged_in'] = True
                session['username'] = email
                session['first_name'] = user.fname

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error = error)
        else:
            error = 'Username %s not found' % (email)
            return render_template('login.html', error = error)

    return render_template('login.html')
# END login


@app.route('/logout')
@app.route('/logout/')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))
# END logout


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
# END is_logged_in


#Dashboard
@app.route('/dashboard')
@app.route('/dashboard/')
@is_logged_in
def dashboard():
    # database connect
    # conn = mysql.connect()
    #
    # # Create cursor
    # cur = conn.cursor()
    #
    # #Get order history
    # result = cur.execute("SELECT * FROM ORDERHISTORY")
    #
    # orders = cur.fetchall(result)
    #
    # if orders > 0:
    #     return render_template('dashboard_order.html', orders=orders)
    # else:
    #     msg = "No order found!"
    #     return  render_template('dashboard_order.html', msg=msg)
    #
    # # Close connection
    # cur.close()

    return render_template('dashboard.html')


def get_chefspecial():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM cuisine")
    return cur.fetchall()


# Sign Up Form Class
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


# SignUp
@app.route('/signup', methods=['GET', 'POST'])
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)

    if request.method == 'POST' and form.validate():
        fname     = form.first_name.data
        lname     = form.last_name.data
        email     = form.email_id.data
        passwd    = sha256_crypt.encrypt(str(form.password.data))
        user_type = form.usertype.data
        aptno     = form.apartment_no.data
        street    = form.street.data
        city      = form.city.data
        state     = form.state.data
        zipcode   = form.zipcode.data
        country   = form.country.data
        phoneno   = form.phone_number.data

        res = create_user(fname, lname, email, passwd, aptno, street, city,
                          state, zipcode, country, phoneno, user_type)

        if (res)
            flash('You are now registered', 'success')
            return redirect(url_for('login'))
        else
            flash('Error in registration', 'failure')
            return render_template('signup.html', form = form)

    return render_template('signup.html', form = form)
# END signup


@app.route('/fooditem')
@app.route('/fooditem/')
def fooditem():
    return render_template('fooditem.html')


@app.route('/orderhistory')
@app.route('/orderhistory/')
def orderhistory():
    return render_template('orderhistory.html')


@app.route('/about')
@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/contactus')
@app.route('/contactus/')
def contactus():
    return render_template('contactus.html')


class OrderPageForm(Form):
    cuisineName = StringField('cuisine', [validators.Length(min=1, max=25)])
    orderDate = StringField('datepicker')
    comments = StringField('comments', [validators.Length(min=1, max=50)])


@app.route('/orderpage', methods=['GET', 'POST'])
def orderpage():
    form = OrderPageForm(request.form)
    if request.method == 'POST' and form.validate():
        return render_template('orderpage.html')
    return render_template('orderpage.html', form=form)


# Sign Up Form Class
class DashboardOrderForm(Form):
    order_name = StringField('What\'s your order', [validators.Length(min=1, max=50)])
    requested_date = DateField('Requested date', format='%m/%d/%Y')
    comments = TextAreaField('Comments', [validators.Length(min=0)])


@app.route('/dashboard_order', methods=['GET', 'POST'])
@is_logged_in
def dashboard_order():
    form = DashboardOrderForm(request.form)
    if request.method == 'POST' and form.validate():
        order_name = form.order_name.data
        requested_date = form.requested_date.data
        comments = form.comments.data
        '''
        When order food is clicked
        page containing chef list based on the location
        should be displayed
        '''
        return redirect(url_for('cheflist'))
    return render_template('dashboard_order.html', form=form)

@app.route('/cheflist', methods=['GET', 'POST'])
def cheflist():
    return render_template('cheflist.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)

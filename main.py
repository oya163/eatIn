import math
import random
import sys

from flask import Flask, session, redirect, g, url_for, escape, request, render_template, flash, logging, abort

from functools import wraps
from passlib.hash import sha256_crypt

from config import *

# app/db config stuff
#app = Flask(__name__)
#app.config["APPLICATION_ROOT"] = APP_ROOT
#app.config['SQLALCHEMY_DATABASE_URI'] = SQL_URI
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#app.secret_key = SEC_KEY

if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')

# routing access
def simple(env, resp):
  resp(b'200 OK', [(b'Content-Type', b'text/plain')])
  return [b'eating']

import models
import forms

from models import app
from models import db

#db.create_all()

@app.route('/')
def index():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html', session_user_name = username_session)
    return redirect(url_for('login'))
# END index


@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form fields
        email = request.form['username']
        password_candidate = request.form['password']

        user = models.get_user_by_email(email)

        if (user != None):
            # Compare passwords
            if sha256_crypt.verify(password_candidate, user.password):
                # Passed
                session['logged_in'] = True
                session['username'] = email
                session['first_name'] = user.fname
                session['userid'] = user.userid

                # set customer and chef ids for convenience
                cust = models.get_customer_by_user(user)
                chef = models.get_chef_by_user(user)

                if (cust):
                    session['custid'] = cust.customerid
                else:
                    session['custid'] = None

                if (chef):
                    session['chefid'] = chef.chefid
                else:
                    session['chefid'] = None

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid credentials'
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


@app.route('/dashboard')
@app.route('/dashboard/')
@is_logged_in
def dashboard():
    print session['userid'], session['custid'], session['chefid']

    # 2 lists of orders per user:
    #   orders as a chef that the user has to carry out
    #   orders as a customer that the user is waiting for
    _orders_as_cust = []
    _orders_as_chef = []

    if (session['custid']):
        _orders_as_cust = models.get_orders_by_customer_id(session['custid'])

    if (session['chefid']):
        _orders_as_chef = models.get_orders_by_customer_id(session['chefid'])

    return render_template('dashboard.html',
                           orders_as_cust = _orders_as_cust,
                           orders_as_chef = _orders_as_chef)
# END dashboard


@app.route('/signup', methods=['GET', 'POST'])
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = forms.SignupForm(request.form)
    form.country.choices = [(c.countryid, c.countryname) for c in models.get_all_countries()]

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

        r = models.create_user(fname, lname, email, passwd, aptno, street, city,
                               state, zipcode, country, phoneno, user_type)

        if (r == 0):
            flash('You are now registered', 'success')
            return redirect(url_for('login'))
        elif (r == 1):
            flash("User with email %s already exists" % (email), 'danger')
            return render_template('signup.html', form = form)

    return render_template('signup.html', form = form)
# END signup


@app.route('/fooditem', methods=['GET'])
@app.route('/fooditem/', methods=['GET'])
@app.route('/fooditem/<foodid>', methods=['GET'])
@is_logged_in
def fooditem(foodid, chefid = None):
    food = models.get_fooditem_by_id(int(foodid))
    chefs = models.get_chefs_by_food_id(foodid)

    return render_template('fooditem.html', food = food,
                                            chefs = chefs)


@app.route('/confirmorder/<foodid>/<chefid>', methods=['GET', 'POST'])
@app.route('/confirmorder/<foodid>/<chefid>/', methods=['GET', 'POST'])
@is_logged_in
def confirmorder(foodid, chefid):
    form = forms.ConfirmOrderForm(request.form)

    food = models.get_fooditem_by_id(int(foodid))
    chef = models.get_chef_by_id(int(chefid))

    if (request.method == 'POST' and form.validate()):
        custid = session['custid']
        req_date = form.requested_date.data.strftime('%Y-%m-%d')
        comment = form.comment.data
        print foodid, chefid, session['custid'], req_date, comment

        models.create_order(custid, chefid, foodid, req_date, comment)

        flash('Order placed.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('confirmorder.html', form = form,
                                                food = food,
                                                chef = chef)


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


@app.route('/account', methods=['GET', 'POST'])
@app.route('/account/', methods=['GET', 'POST'])
@is_logged_in
def account():
    form = forms.AccountForm(request.form)
    form.country.choices = [(c.countryid, c.countryname) for c in models.get_all_countries()]
    form.chefspec.choices = [(c.cuisineid, c.cuisine_name) for c in models.get_all_cuisines()]
    form.custpref.choices = [(c.cuisineid, c.cuisine_name) for c in models.get_all_cuisines()]

    # populate form with existing info
    user = models.get_user_by_id(session['userid'])
    chef = models.get_chef_by_id(session['chefid'])
    cust = models.get_customer_by_id(session['custid'])

    if (request.method == 'POST' and form.validate()):
        fname     = form.first_name.data
        lname     = form.last_name.data
        email     = form.email_id.data
        passwd    = sha256_crypt.encrypt(str(form.password.data))
        user_type = form.usertype.data
        aptno     = form.apartment_no.data
        street    = form.street.data
        city      = form.city.data
        state     = form.state.data
        zipcode   = int(form.zipcode.data)
        country   = int(form.country.data)
        phoneno   = int(form.phone_number.data)
        chefspec  = int(form.chefspec.data)
        custpref  = form.custpref.data

        # update with new info if necessary
        r = user.update(fname, lname, email, passwd, user_type, aptno, street,
                        city, state, zipcode, country, phoneno, chefspec,
                        custpref)

        if (r == 0):
            flash('User details updated', 'success')
        else:
            flash('Update failed', 'danger')

        return render_template('account.html', form = form,
                                               chef = chef,
                                               cust = cust)

    # figure out the user type and prefill fields with existing info
    # probably a better way to do this but whatever
    usertype = ""
    aptno, street, city, state, zipcode, countryid, phoneno = (None,)*7
    chefspec = None
    custpref = None
    if (chef and cust):
        usertype  = "both"
        aptno     = chef.address
        street    = chef.street
        city      = chef.city
        state     = chef.state
        zipcode   = chef.zipcode
        countryid = chef.countryid
        phoneno   = chef.phone_number
        chefspec  = chef.get_speciality()
        custpref  = cust.preference
    elif (chef):
        usertype  = "chef"
        aptno     = chef.address
        street    = chef.street
        city      = chef.city
        state     = chef.state
        zipcode   = chef.zipcode
        countryid = chef.countryid
        phoneno   = chef.phone_number
        chefspec  = chef.get_speciality()
    elif (cust):
        usertype  = "customer"
        aptno     = cust.address
        street    = cust.street
        city      = cust.city
        state     = cust.state
        zipcode   = cust.zipcode
        countryid = cust.countryid
        phoneno   = cust.phone_number
        custpref  = cust.preference

    form.first_name.data = user.fname
    form.last_name.data  = user.lname
    form.email_id.data   = user.email
    form.password.data   = None
    form.usertype.data   = usertype

    form.apartment_no.data = aptno
    form.street.data       = street
    form.city.data         = city
    form.state.data        = state
    form.zipcode.data      = str(zipcode)
    form.country.data      = countryid
    form.phone_number.data = str(phoneno)

    return render_template('account.html', form = form,
                                           chef = chef,
                                           cust = cust)
# END account

# TODO: delete this later, using dashboard_order instead
@app.route('/orderpage', methods=['GET', 'POST'])
def orderpage():
    # to place an order:
    #   - first pick a cuisine type
    #   - then pick a meal
    #   - then pick a chef and time
    form = forms.OrderPageForm(request.form)
    form.cuisine.choices = [(c.cuisineid, c.cuisine_name) for c in models.get_all_cuisines()]

    if (request.method == 'POST' and form.validate()):
        return render_template('orderpage.html')

    return render_template('orderpage.html', form = form)


@app.route('/dashboard_order', methods=['GET', 'POST'])
@app.route('/dashboard_order/', methods=['GET', 'POST'])
@is_logged_in
def dashboard_order():
    form = forms.DashboardOrderForm(request.form)
    form.cuisine.choices = [(c.cuisineid, c.cuisine_name) for c in models.get_all_cuisines()]

    if (request.method == 'POST' and form.validate()):
        cuisineid = form.cuisine.data
        print cuisineid
        foods = models.get_fooditems_by_cuisine_id(cuisineid)

        return render_template('dashboard_order.html', form = form,
                                                       foods = foods)

    return render_template('dashboard_order.html', form = form,
                                                   foods = [])

@app.route('/cheflist', methods=['GET', 'POST'])
def cheflist():
    return render_template('cheflist.html')


@app.route('/meallist', methods=['GET', 'POST'])
@app.route('/meallist/', methods=['GET', 'POST'])
def meallist():
    return render_template('cheflist.html')



if __name__ == '__main__':
    app.run(host = "127.0.0.1", port = 5050, debug = True)

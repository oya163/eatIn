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
    if ('username' in session):
        return render_template('index.html',
                               session_user_name = session['username'])

    # redirct to login page if not logged in
    return redirect(url_for('login'))
# END index


@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password_candidate = request.form['password']

        user = models.get_user_by_email(email)

        if (user != None):
            if sha256_crypt.verify(password_candidate, user.password):
                update_session(user)

                flash('You are now logged in', 'success')
                return render_template('index.html',
                                       session_user_name = session['username'])
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
        _orders_as_chef = models.get_orders_by_chef_id(session['chefid'])

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
# END fooditem


@app.route('/chef', methods=['GET'])
@app.route('/chef/', methods=['GET'])
@app.route('/chef/<chefid>', methods=['GET'])
@is_logged_in
def chef(chefid, foodid = None):
    chef = models.get_chef_by_id(chefid)
    foods = models.get_fooditems_by_chef_id(int(chefid))

    return render_template('chef.html', chef = chef,
                                        foods = foods)
# END chef


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
# END confirmorder


@app.route('/cancelorder/<orderid>', methods=['GET'])
@app.route('/cancelorder/<orderid>/', methods=['GET'])
@is_logged_in
def cancelorder(orderid):
    order = models.get_order_by_id(int(orderid))
    print order

    if (session['chefid'] == order.chefid):
        models.cancel_order(order, "chef")
        flash('Order cancelled.', 'success')

    elif (session['custid'] == order.customerid):
        models.cancel_order(order, "customer")
        flash('Order cancelled.', 'success')

    else:
        flash('Order not changed', 'danger')

    return redirect(url_for('dashboard'))
# END cancelorder


@app.route('/completeorder/<orderid>', methods=['GET'])
@app.route('/completeorder/<orderid>/', methods=['GET'])
@is_logged_in
def completeorder(orderid):
    order = models.get_order_by_id(int(orderid))
    print order

    if (session['chefid'] == order.chefid):
        models.cancel_order(order, "chef")
        flash('Order completed.', 'success')

    else:
        flash('Order not changed', 'danger')

    return redirect(url_for('dashboard'))
# END completeorder


@app.route('/orderinfo/<orderid>', methods=['GET', 'POST'])
@app.route('/orderinfo/<orderid>/', methods=['GET', 'POST'])
@is_logged_in
def orderinfo(orderid):
    form = forms.UpdateOrderForm(request.form)

    order = models.get_order_by_id(int(orderid))
    food = models.get_fooditem_by_id(order.foodid)
    chef = models.get_chef_by_id(order.chefid)
    cust = models.get_customer_by_id(order.customerid)

    print order, food, chef, cust

    if (request.method == 'POST' and form.validate()):
        comment = form.comment.data
        order.update_comment(comment)

        if (session['chefid'] == chef.chefid):
            flash('You are the CHEF of this order!', 'success')
        elif (session['custid'] == cust.customerid):
            flash('You are the CUSTOMER of this order!', 'success')

        flash('Order comment updated', 'success')

        return render_template('orderinfo.html', form = form,
                                                 order = order,
                                                 food = food,
                                                 chef = chef,
                                                 cust = cust)

    form.comment.data = order.comment

    if (session['chefid'] == chef.chefid):
        flash('You are the CHEF of this order!', 'success')
    elif (session['custid'] == cust.customerid):
        flash('You are the CUSTOMER of this order!', 'success')

    return render_template('orderinfo.html', form = form,
                                             order = order,
                                             food = food,
                                             chef = chef,
                                             cust = cust)
# END orderinfo


@app.route('/orderhistory')
@app.route('/orderhistory/')
def orderhistory():
    return render_template('orderhistory.html')


@app.route('/about')
@app.route('/about/')
def about():
    return render_template('about.html')
# END about


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
    form.chefspec.choices.append((-1, "Pick a Specialty..."))
    #form.custpref.choices = [(c.cuisineid, c.cuisine_name) for c in models.get_all_cuisines()]

    # populate form with existing info
    user = models.get_user_by_id(session['userid'])
    chef = models.get_chef_by_id(session['chefid'])
    cust = models.get_customer_by_id(session['custid'])

    print form.first_name.data, form.last_name.data
    print form.country.data, form.usertype.data
    print request.method, form.validate()

    if (request.method == 'POST'):
        print request.form

        # delete chef/cust only options from the form to get through validation
        if (not chef):
            del form.chefspec
        if (not cust):
            del form.custpref

        if (form.validate()):
            print "posting..."
            fname     = form.first_name.data
            lname     = form.last_name.data
            email     = form.email_id.data
            passwd    = sha256_crypt.encrypt(str(form.password.data))
            user_type = form.usertype.data
            aptno     = form.apartment_no.data
            street    = form.street.data
            city      = form.city.data
            state     = form.state.data
            zipcode   = int(form.zipcode.data) if form.zipcode.data else None
            country   = int(form.country.data) if form.country.data else None
            phoneno   = int(form.phone_number.data) if form.phone_number.data else None
            chefspec  = None
            reachouts = None
            custpref  = None

            if (chef):
                chefspec  = int(form.chefspec.data)
                reachouts = form.reachouts.data
            if (cust):
                custpref  = form.custpref.data

            # update with new info if necessary
            r = user.update(fname, lname, email, passwd, user_type, aptno, street,
                            city, state, zipcode, country, phoneno, chefspec,
                            reachouts, custpref)

            update_session(user)

            if (r == 0):
                flash('User details updated. Visit account page again to see new fields', 'success')
            else:
                flash('Update failed, check the submitted data for errors', 'danger')

            return render_template('account.html', form = form,
                                                   chef = chef,
                                                   cust = cust)
        else:
            flash('Update failed, check the submitted data for errors', 'danger')
            return render_template('account.html', form = form,
                                                   chef = chef,
                                                   cust = cust)

    elif (request.method == 'GET'):
        usertype = ""
        aptno, street, city, state, zipcode, countryid, phoneno = (None,)*7
        chefspec = None
        custpref = None
        reachouts = None
        if (chef and cust):
            usertype  = "both"
            aptno     = chef.address
            street    = chef.street
            city      = chef.city
            state     = chef.state
            zipcode   = chef.zipcode
            countryid = chef.countryid
            phoneno   = chef.phone_number
            chefspec  = chef.get_specialty()
            reachouts = chef.get_reachouts_str()
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
            chefspec  = chef.get_specialty()
            reachouts = chef.get_reachouts_str()
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

        form.chefspec.data     = chefspec.cuisineid if chefspec else -1
        form.reachouts.data    = reachouts
        form.custpref.data     = custpref

        if (not chef):
            del form.chefspec
            del form.reachouts
        if (not cust):
            del form.custpref

        return render_template('account.html', form = form,
                                               chef = chef,
                                               cust = cust)
    flash('Update failed', 'danger')
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
    return render_template('dashboard_order.html')
# END dashboard_order


@app.route('/statistics', methods=['GET'])
@app.route('/statistics/', methods=['GET'])
@is_logged_in
def statistics():
    chefs = models.get_most_popular_chefs()
    foods = models.get_most_popular_foods()
    cuisines = models.get_most_popular_cuisines()

    print chefs
    print foods
    print cuisines

    return render_template('statistics.html', chefs = chefs,
                                              foods = foods,
                                              cuisines = cuisines)
# END statistics


@app.route('/cheflist', methods=['GET', 'POST'])
@app.route('/cheflist/', methods=['GET', 'POST'])
@is_logged_in
def cheflist():
    form = forms.FindChefForm(request.form)
    form.country.choices = [(c.countryid, c.countryname) for c in models.get_all_countries()]

    if (request.method == 'POST' and form.validate()):
        countryid = form.country.data
        print countryid
        chefs = models.get_chefs_by_countryid(countryid)

        return render_template('cheflist.html', form = form,
                                                chefs = chefs)

    return render_template('cheflist.html', form = form,
                                            chefs = [])
# END cheflist


@app.route('/foodlist', methods=['GET', 'POST'])
@app.route('/foodlist/', methods=['GET', 'POST'])
@is_logged_in
def foodlist():
    form = forms.FindFoodForm(request.form)
    form.cuisine.choices = [(c.cuisineid, c.cuisine_name) for c in models.get_all_cuisines()]

    if (request.method == 'POST' and form.validate()):
        cuisineid = form.cuisine.data
        print cuisineid
        foods = models.get_fooditems_by_cuisine_id(cuisineid)

        return render_template('foodlist.html', form = form,
                                                foods = foods)

    return render_template('foodlist.html', form = form,
                                            foods = [])
# END foodlist


def update_session(user):
    session['logged_in'] = True
    session['username'] = user.email
    session['first_name'] = user.fname
    session['userid'] = user.userid

    user = models.get_user_by_id(session['userid'])
    session['userid'] = user.userid

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
# END update_session


if __name__ == '__main__':
    app.run(host = "127.0.0.1", port = 5050, debug = True)

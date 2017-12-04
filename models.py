import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import text
from sqlalchemy import join
from sqlalchemy import select
from sqlalchemy.sql import text

from config import *

# app/db config stuff
app = Flask(__name__)
app.config["APPLICATION_ROOT"] = APP_ROOT
app.config['SQLALCHEMY_DATABASE_URI'] = SQL_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = SEC_KEY

db = SQLAlchemy(app)

class Chef(db.Model):
    __tablename__ = 'chef'

    chefid = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100))
    street = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zipcode = db.Column(db.Integer)
    countryid = db.Column(db.Integer, db.ForeignKey('country.countryid'))
    phone_number = db.Column(db.Integer)
    rating = db.Column(db.Float)
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))
    chefdbid = db.Column(db.Integer)

    def __init__(self, address, street, city, state, zipcode, countryid, phone_number, rating, userid, chefdbid):
        self.address = address    # aka apt_no or whatever
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.countryid = countryid
        self.phone_number = phone_number
        self.rating = rating
        self.userid = userid
        self.chefdbid = chefdbid

    def __repr__(self):
        return '<ChefID %r>' % self.chefid

    def update(self, _aptno, _street, _city, _state, _zipcode,
               _countryid, _phoneno, _cspec, _reachouts_str):
        if (_aptno and _aptno != self.address):
            self.address = _aptno

        if (_street and _street != self.street):
            self.street = _street

        if (_city and _city != self.city):
            self.city = _city

        if (_state and _state != self.state):
            self.state = _state

        if (_zipcode and _zipcode != self.zipcode):
            self.zipcode = _zipcode

        if (_countryid and _countryid != self.countryid):
            self.countryid = _countryid

        if (_phoneno and _phoneno != self.phone_number):
            self.phone_number = _phoneno

        if (_cspec):
            print "in cspec"
            cspecm = self.get_specialty_mapping()

            if (cspecm):
                cspecm.cuisineid = _cspec
            else:
                cspecm = ChefSpecial(self.chefid, _cspec)
                db.session.add(cspecm)

        if (_reachouts_str):
            print "in reachouts"
            reachouts_str = self.get_reachouts_str()

            if (reachouts_str != _reachouts_str):
                add_reachouts_by_str(self.chefid, _reachouts_str)

        return 0

    def get_user(self):
        return get_user_by_id(self.userid)

    def get_specialty(self):
        chefspec = ChefSpecial.query.filter_by(chefid = self.chefid).first()
        if (chefspec != None):
            cuisine = Cuisine.query.filter_by(cuisineid = chefspec.cuisineid).first()
            return cuisine
        else:
            return None

    def get_specialty_id(self):
        chefspec = self.get_specialty()
        if (chefspec != None):
            cuisine = Cuisine.query.filter_by(cuisineid = chefspec.cuisineid).first()
            return cuisine.cuisineid
        else:
            return -1

    def get_specialty_mapping(self):
        return ChefSpecial.query.filter_by(chefid = self.chefid).first()

    def get_reachouts(self):
        return ChefReachout.query.filter_by(chefid = self.chefid).all()

    def get_country(self):
        return Country.query.filter_by(countryid = self.countryid).first()

    def get_full_name(self):
        return get_user_by_id(self.userid).fname + " " + get_user_by_id(self.userid).lname

    def get_reachouts_str(self, single_line = False):
        reachouts = get_reachouts_list_by_chefid(self.chefid)

        # set delimiter
        DELIM = ", " if single_line else "\n"

        reachouts_str = ""

        if (reachouts == None or len(reachouts) == 0):
            return reachouts_str

        for r in reachouts:
            reachouts_str = reachouts_str + r.city + DELIM

        return reachouts_str.strip()

    def get_reachouts_list(self):
        return get_reachouts_list_by_chefid(self.chefid)
# END Chef

def get_chef_by_user(_user):
    chef = Chef.query.filter_by(userid = _user.userid).first()
    return chef
# END get_chef_by_user

def get_chef_by_id(_chefid):
    chef = Chef.query.filter_by(chefid = _chefid).first()
    return chef
# END get_chef_by_id

def get_all_chefs():
    return Chef.query.order_by(Chef.chefid).all()
# END get_all_chefs

def get_chefs_by_countryid(_countryid):
    return Chef.query.filter_by(countryid = _countryid).all()
# END get_chefs_by_countryid


class ChefReachout(db.Model):
    __tablename__ = 'chefreachout'

    reachoutid = db.Column(db.Integer, primary_key=True)
    chefid = db.Column(db.Integer, db.ForeignKey('chef.chefid'), primary_key=True)
    city = db.Column(db.String(50))
    miles = db.Column(db.Integer)

    def __init__(self, chefid, city, miles):
        self.chefid = chefid
        self.city = city
        self.miles

    def __repr__(self):
        return '<RO %r>' % (self.reachoutid)
# END ChefReachout

def get_reachouts_list_by_chefid(_chefid):
    return ChefReachout.query.filter_by(chefid = _chefid).distinct().all()
# END get_reachouts_list_by_chefid

def add_reachouts_by_str(_chefid, _str):
    # delete existing reachout data
    db.engine.execute(text("CALL delete_chef_reachouts(%s)" % (_chefid)))

    # add new ones
    reachouts = _str.split("\n")
    for r in reachouts:
        ro = ChefReachout(_chefid, r.strip(), 0)
        db.session.add(ro)
    db.session.commit()

    return 0
# END add_reachouts_by_str


class ChefSpecial(db.Model):
    __tablename__ = 'chefspecial'

    chefid = db.Column(db.Integer, db.ForeignKey('chef.chefid'), primary_key=True)
    cuisineid = db.Column(db.Integer, db.ForeignKey('cuisine.cuisineid'), primary_key=True)

    def __init__(self, chefid, cuisineid):
        self.chefid = chefid
        self.cuisineid = cuisineid

    def __repr__(self):
        return '<ChefID %r CuisineID %r>' % (self.chefid, self.cuisineid)
# END ChefSpecial

def get_chef_specials_by_chef_id(_chefid):
    cspecs = ChefSpecial.query.filter_by(chefid = _chefid).all()

    cuisines = []
    for cspec in cspecs:
        cuisine = Cuisine.query.filter_by(cuisineid = cspec.cuisineid).first()
        cuisines.append(cuisine)

    return cuisines
# END get_chef_specials_by_chef_id

def get_chefs_by_cuisine_id(_cuisineid):
    stmt = "SELECT * " \
           "FROM chefspecial JOIN chef ON chefspecial.chefid = chef.chefid " \
           "WHERE cuisineid = %s" % (str(_cuisineid))

    res = db.engine.execute(text(stmt))
    chefs = []
    for r in res:
        chefs.append(r)

    return chefs
# END get_chefs_by_cuisine_id

# return format is: [userid, chefid, fname, lname, countryid, countryname]
def get_chefs_by_food_id(_foodid):
    stmt = "CALL get_chefs_by_food_id(%s)" % (_foodid)

    #stmt = "SELECT chef.userid, chef.chefid, user.fname, user.lname, country.countryid, country.countryname " \
    #       "FROM (((chefspecial JOIN chef ON chefspecial.chefid = chef.chefid) " \
    #       "  JOIN cuisineitem ON cuisineitem.cuisineid = chefspecial.cuisineid) " \
    #       "  JOIN user ON user.userid = chef.userid) " \
    #       "  JOIN country ON chef.countryid = country.countryid " \
    #       "WHERE cuisineitem.foodid = %s" % (_foodid)

    res = db.engine.execute(text(stmt))
    chefs = []
    for r in res:
        chefs.append(r)

    return chefs
# END get_chefs_by_food_id

# return format is:
# [userid, chefid, fname, lname, countryid, countryname, cuisineid, cuisinename]
def get_chef_details_list():
    stmt = "CALL get_all_chefs_details()"

    #stmt = "SELECT chef.userid, chef.chefid, user.fname, user.lname," \
    #       " country.countryid, country.countryname, cuisine.cuisineid, cuisine.cuisine_name " \
    #       "FROM (((chef JOIN country ON chef.countryid = country.countryid) " \
    #       "  JOIN chefspecial ON chefspecial.chefid = chef.chefid) " \
    #       "  JOIN cuisine ON chefspecial.cuisineid = cuisine.cuisineid) "\
    #       "  JOIN user ON user.userid = chef.userid"

    res = db.engine.execute(text(stmt))
    chefs = []
    for r in res:
        chefs.append(r)

    return chefs
# END get_chef_details_list


class Country(db.Model):
    __tablename__ = 'country'

    countryid = db.Column(db.Integer, primary_key=True)
    countryname = db.Column(db.String(100))
    abbr = db.Column(db.String(3))

    def __init__(self, countryname, abbr):
        self.countryname = countryname
        self.abbr = abbr

    def __repr__(self):
        return '<CountryID %r>' % (self.countryid)
# END Country

def get_country_id_by_name(_countryname):
    country = Country.query.filter_by(countryname = _countryname).first()  
    return country
# END get_country_id_by_name

def get_all_countries():
    countries = Country.query.order_by(Country.countryname).all()
    return countries
# END get_all_countries


class Cuisine(db.Model):
    __tablename__ = 'cuisine'

    cuisineid = db.Column(db.Integer, primary_key=True)
    cuisine_name = db.Column(db.String(50))

    def __init__(self, cuisine_name):
        self.cuisine_name = cuisine_name

    def __repr__(self):
        return '<CuisineID %r>' % self.cuisineid
# END Cuisine

def get_all_cuisines():
    cuisines = Cuisine.query.order_by(Cuisine.cuisineid).all()
    return cuisines
# END get_all_cuisines


class Customer(db.Model):
    __tablename__ = 'customer'

    customerid = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100))
    street = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zipcode = db.Column(db.Integer)
    countryid = db.Column(db.Integer, db.ForeignKey('country.countryid'))
    phone_number = db.Column(db.Integer)
    preference = db.Column(db.String(500))
    userid = db.Column(db.Integer, db.ForeignKey('user.userid'))

    def __init__(self, address, street, city, state, zipcode, countryid, phone_number, preference, userid):
        self.address = address    # aka apt_no or whatever
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.countryid = countryid
        self.phone_number = phone_number
        self.preference = preference
        self.userid = userid

    def __repr__(self):
        return '<CustomerID %r>' % self.customerid

    def update(self, _aptno, _street, _city, _state, _zipcode,
               _countryid, _phoneno, _pref):
        self.address = _aptno
        self.street = _street
        self.city = _city
        self.state = _state
        self.zipcode = _zipcode
        self.countryid = _countryid
        self.phone_number = _phoneno
        self.preference = _pref

        return 0

    def get_user(self):
        return get_user_by_id(self.userid)
# END Customer

def get_customer_by_user(_user):
    cust = Customer.query.filter_by(userid = _user.userid).first()
    return cust
# END get_customer_by_user

def get_customer_by_id(_custid):
    cust = Customer.query.filter_by(customerid = _custid).first()
    return cust
# END get_customer_by_id

def get_all_customers():
    return Customer.query.order_by(Customer.customerid).all()
# END get_all_customers


class FoodItem(db.Model):
    __tablename__ = 'fooditem'

    foodid = db.Column(db.Integer, primary_key=True)
    foodname = db.Column(db.String(200))
    food_des = db.Column(db.String(500))
    cook_time = db.Column(db.Integer)
    food_rating = db.Column(db.Float)
    price = db.Column(db.Float)
    fn_id = db.Column(db.String(10))

    def __init__(self, foodname, food_des, cook_time, food_rating, price, fn_id):
        self.foodname = foodname
        self.food_des = food_des
        self.cook_time = cook_time
        self.food_rating = food_rating
        self.price = price
        self.fn_id = fn_id

    def __repr__(self):
        return '<FoodID %r>' % self.foodid
# END FoodItem

def get_fooditem_by_id(_foodid):
    food = FoodItem.query.filter_by(foodid = _foodid).first()
    return food
# END get_fooditem_by_id

def get_all_fooditems():
    return FoodItem.query.order_by(FoodItem.foodname).all()
# END get_all_fooditems


class CuisineItem(db.Model):
    __tablename__ = 'cuisineitem'

    foodid = db.Column(db.Integer, db.ForeignKey('fooditem.foodid'), primary_key=True)
    cuisineid = db.Column(db.Integer, db.ForeignKey('cuisine.cuisineid'), primary_key=True)

    def __init__(self, foodid, cuisineid):
        self.foodid = foodid
        self.cuisineid = cuisineid

    def __repr__(self):
        return '<FoodID %r CuisineID %r>' % (self.foodid, self.cuisineid)
# END CuisineItem

# This actually doesn't return a list of FoodItem objects, but instead a list
# with indicies that correspond to the column numbers from executing the sql
# query below through mysql. This is because we are executing a raw SQL stmt
# without any mapping to the ORM.
def get_fooditems_by_cuisine_id(_cuisineid):
    stmt = "SELECT * " \
           "FROM cuisineitem JOIN fooditem ON cuisineitem.foodid = fooditem.foodid " \
           "WHERE cuisineid = %s" % (str(_cuisineid))

    res = db.engine.execute(text(stmt))
    foods = []
    for r in res:
        foods.append(r)

    return foods
# END get_fooditems_by_cuisine_id

def get_fooditems_by_chef_id(_chefid):
    return get_fooditems_by_cuisine_id(get_chef_by_id(_chefid).get_specialty().cuisineid)
# END get_fooditems_by_cuisine_id


class User(db.Model):
    __tablename__ = 'user'

    userid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(100))
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    user_type = db.Column(db.String(20))

    def __init__(self, email, password, fname, lname, user_type):
        self.email = email
        self.password = password
        self.fname = fname
        self.lname = lname
        self.user_type = user_type

    def __repr__(self):
        return '<UserID %r>' % self.userid

    def update(self, _fname, _lname, _email, _passwd, _utype, _aptno, _street,
               _city, _state, _zipcode, _countryid, _phoneno, _chefspecid, 
               _reachouts, _custpref):

        if (_email and _email != self.email and len(_email) > 6):
             if (get_user_by_email(_email) == None):
                 self.email = _email
                 return 1

        # don't want to figure out password right now
        if (_passwd):
            pass

        if (_fname and _fname != self.fname and len(_fname) > 0):
            self.fname = _fname

        if (_lname and _lname != self.lname and len(_lname) > 0):
            self.lname = _lname

        if (_utype == "both"):
            print "type = both"
            # find existing chef/cust entities
            chef = get_chef_by_user(self)
            cust = get_customer_by_user(self)
            print chef, cust

            # update existing chef entity if it already exists, otherwise make
            # a new one
            if (chef):
                chef.update(_aptno, _street, _city, _state, _zipcode,
                            _countryid, _phoneno, _chefspecid, _reachouts)
                print "updated old chef", chef.chefid
            else:
                chef = Chef(_aptno, _street, _city, _state, _zipcode,
                            _countryid, _phoneno, None, self.userid, None)
                db.session.add(chef)
                print "added new chef"

            # same for customer
            if (cust):
                cust.update(_aptno, _street, _city, _state, _zipcode,
                            _countryid, _phoneno, _custpref)
                print "updated old cust", cust.customerid
            else:
                cust = Customer(_aptno, _street, _city, _state, _zipcode,
                                _countryid, _phoneno, _custpref, self.userid)
                db.session.add(cust)
                print "added new cust"
        elif (_utype == "customer"):
            print "type = cust"
            # find existing chef/cust entities
            chef = get_chef_by_user(self)
            cust = get_customer_by_user(self)

            if (chef):
                db.engine.execute(text("CALL delete_chef(%s)" % (chef.chefid)))

            # now update old/make new customer
            if (cust):
                cust.update(_aptno, _street, _city, _state, _zipcode,
                            _countryid, _phoneno, _custpref)
            else:
                cust = Customer(_aptno, _street, _city, _state, _zipcode,
                                _countryid, _phoneno, _custpref, self.userid)
                db.session.add(cust)
        elif (_utype == "chef"):
            chef = get_chef_by_user(self)
            cust = get_customer_by_user(self)

            if (cust):
                db.engine.execute(text("CALL delete_customer(%s)" % (cust.customerid)))

            # now update/create chef
            if (chef):
                chef.update(_aptno, _street, _city, _state, _zipcode,
                            _countryid, _phoneno, _chefspecid, _reachouts)
            else:
                chef = Chef(_aptno, _street, _city, _state, _zipcode,
                            _countryid, _phoneno, None, self.userid, None)
                db.session.add(chef)

        db.session.commit()
        return 0
# END User

def get_user_by_email(_email):
    user = User.query.filter_by(email = _email).first()
    return user
# END get_user_by_email

def get_user_by_id(_userid):
    user = User.query.filter_by(userid = _userid).first()
    return user
# END get_user_by_id

def get_all_users():
    return User.query.order_by(userid).all()
# END get_all_users

def create_user(fname, lname, email, passwd, aptno, street, city, state,
                zipcode, countryid, phoneno, user_type):
    # create user first
    print "creating user:", fname, lname, email, passwd, aptno, street, city, state, zipcode, countryid, phoneno, user_type

    # first check if user already exists
    u = get_user_by_email(email)
    if (u != None):
        return 1

    user = User(email, passwd, fname, lname, user_type)
    db.session.add(user)
    db.session.commit()

    user_id = user.userid
    zipcode = int(zipcode) if zipcode else 0
    phoneno = int(phoneno) if phoneno else 0

    # now create customer/chef
    if (user_type == "customer"):
        customer = Customer(aptno, street, city, state, zipcode, countryid, phoneno, None, user_id)
        db.session.add(customer)
    elif (user_type == "chef"):
        chef = Chef(aptno, street, city, state, zipcode, countryid, phoneno, None, user_id, None)
        db.session.add(chef)
    elif (user_type == "both"):
        customer = Customer(aptno, street, city, state, zipcode, countryid, phoneno, None, user_id)
        db.session.add(customer)
        chef = Chef(aptno, street, city, state, zipcode, countryid, phoneno, None, user_id, None)
        db.session.add(chef)

    db.session.commit()

    return 0
# END create_user


class OrderFood(db.Model):
    __tablename__ = 'orderfood'

    orderid = db.Column(db.Integer, primary_key=True)
    customerid = db.Column(db.Integer, db.ForeignKey('customer.customerid'))
    chefid = db.Column(db.Integer, db.ForeignKey('chef.chefid'))
    foodid = db.Column(db.Integer, db.ForeignKey('fooditem.foodid'))
    order_date = db.Column(db.DateTime)
    req_date = db.Column(db.DateTime)
    comment = db.Column(db.String(300))

    def __init__(self, customerid, chefid, foodid, order_date, req_date, comment):
        self.customerid = customerid
        self.chefid = chefid
        self.foodid = foodid
        self.order_date = order_date
        self.req_date = req_date
        self.comment = comment

    def __repr__(self):
        return '<OrderID %r>' % self.orderid

    def get_food(self):
        return get_fooditem_by_id(self.foodid)

    def get_chef(self):
        return get_chef_by_id(self.chefid)

    def get_customer(self):
        return get_customer_by_id(self.customerid)
# END OrderFood

def get_orders_by_customer_id(_custid):
    orders = OrderFood.query.filter_by(customerid = _custid).all()
    return orders
# END get_orders_by_customer_id

def get_orders_by_chef_id(_chefid):
    orders = OrderFood.query.filter_by(chefid = _chefid).all()
    return orders
# END get_orders_by_chef_id

def create_order(_custid, _chefid, _foodid, _req_date, _comment):
    order_date = datetime.datetime.now()
    print order_date

    order = OrderFood(_custid, _chefid, _foodid, order_date, _req_date, _comment)
    db.session.add(order)
    db.session.commit()

    return 0
# END create_order


# Counter tables (read only)
class FoodItemCnt(db.Model):
    __tablename__ = 'fooditem_cnt'

    foodid = db.Column(db.Integer, db.ForeignKey('fooditem.foodid'), primary_key = True)
    counter = db.Column(db.Integer)

    def __repr__(self):
        return '<FoodID %r>' % self.foodid
# END FoodItemCnt

# return format is: [foodid, name, cook time, rating, price, counter] 
def get_most_popular_foods():
    LIM = 100
    stmt = "CALL get_most_popular_foods(%d)" % (LIM)

    #stmt = "SELECT fooditem.foodid, fooditem.foodname, fooditem.cook_time, " \
    #       "  fooditem.food_rating, fooditem.price, fooditem_cnt.counter " \
    #       "FROM fooditem_cnt JOIN fooditem ON fooditem.foodid = fooditem_cnt.foodid " \
    #       "ORDER BY counter " \
    #       "LIMIT 100"
    
    res = db.engine.execute(text(stmt))
    foods = []
    for r in res:
        foods.append(r)

    return foods
# END get_most_popular_foods


class ChefCnt(db.Model):
    __tablename__ = 'chef_cnt'

    chefid = db.Column(db.Integer, db.ForeignKey('chef.chefid'), primary_key = True)
    counter = db.Column(db.Integer)

    def __repr__(self):
        return '<ChefID %r>' % self.chefid
# END ChefCnt

# return format is: [userid, chefid, fname, lname, countryid, countryname, cuisineid,
#                    cuisine_name, counter]
def get_most_popular_chefs():
    LIM = 100
    stmt = "CALL get_most_popular_chefs(%d)" % (LIM)

    #stmt = "SELECT chef.userid, chef.chefid, user.fname, user.lname," \
    #       " country.countryid, country.countryname, cuisine.cuisineid, cuisine.cuisine_name, " \
    #       " chef_cnt.counter " \
    #       "FROM ((((chef JOIN country ON chef.countryid = country.countryid) " \
    #       "  JOIN chefspecial ON chefspecial.chefid = chef.chefid) " \
    #       "  JOIN cuisine ON chefspecial.cuisineid = cuisine.cuisineid) " \
    #       "  JOIN user ON user.userid = chef.userid) " \
    #       "  JOIN chef_cnt ON chef_cnt.chefid = chef.chefid " \
    #       "ORDER BY counter " \
    #       "LIMIT 100"

    #stmt = "SELECT  " \
    #       "FROM (((chef_cnt JOIN chef ON chef.chefid = chef_cnt.chefid " \
    #       "ORDER BY counter " \
    #       "LIMIT 100"

    res = db.engine.execute(text(stmt))
    chefs = []
    for r in res:
        chefs.append(r)

    return chefs
# END get_most_popular_chefs


class CuisineCnt(db.Model):
    __tablename__ = 'cuisine_cnt'

    cuisineid = db.Column(db.Integer, db.ForeignKey('cuisine.cuisineid'), primary_key = True)
    counter = db.Column(db.Integer)

    def __repr__(self):
        return '<CuisineID %r>' % self.cuisineid
# END CuisineCnt

# return format is: [cuisineid, cuisine_name, counter]
def get_most_popular_cuisines():
    LIM = 100
    stmt = "CALL get_most_popular_cuisines(%d)" % (LIM)

    res = db.engine.execute(text(stmt))
    cuisines = []
    for r in res:
        cuisines.append(r)

    return cuisines
# END get_most_popular_cuisines

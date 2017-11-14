from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

from main import app

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
        self.address = address
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
# END Chef


class ChefReachout(db.Model):
    __tablename__ = 'chefreachout'

    chefid = db.Column(db.Integer, db.ForeignKey('chef.chefid'), primary_key=True)
    city = db.Column(db.String(50))
    miles = db.Column(db.Integer)

    def __init__(self, chefid, city):
        self.chefid = chefid
        self.city = city
        self.miles

    def __repr__(self):
        return '<ChefID %r City %s Miles %r>' % (self.chefid, self.city, self.miles)
# END ChefReachout


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
        self.address = address
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.countryid = countryid
        self.phone_number = phone_number
        self.preference = preference
        self.userid = userid

    def __repr__(self):
        return '<CustomerID %r>' % self.cutomerid
# END Customer


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


class CuisineItem(db.Model):
    __tablename__ = 'cuisineitem'

    foodid = db.Column(db.Integer, db.ForeignKey('fooditem.foodid'), primary_key=True)
    cuisineid = db.Column(db.Integer, db.ForeignKey('cuisine.cuisineid'), primary_key=True)

    def __init__(self, foodid, cuisineid):
        self.chefid = foodid
        self.cuisineid = cuisineid

    def __repr__(self):
        return '<FoodID %r CuisineID %r>' % (self.foodid, self.cuisineid)
# END CuisineItem


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
# END User

def get_user_by_email(_email):
    user = User.query.filter_by(email = _email).first()
    return user
# END get_user_by_email

def create_user(fname, lname, email, passwd, aptno, street, city, state, zipcode, country, phoneno, user_type):
    # create user first
    user = User(email, passwd, fname, lname, user_type)
    db.session.add(user)
    user_id = user.userid

    countryid = get_country_id_by_name(country).countryid

    # now create customer/chef
    if (type == "customer"):
        customer = Customer(aptno, street, city, state, zipcode, countryid, phone_number, None, userid)
        db.session.add(customer)

    elif (type == "chef"):
        chef = Chef(aptno, street, city, state, zipcode, countryid, phone_number, None, userid, None)
        db.session.add(chef)

    db.session.commit()

    return True
# END create_user


class OrderFood(db.Model):
    __tablename__ = 'orderfood'

    orderid = db.Column(db.Integer, primary_key=True)
    customerid = db.Column(db.Integer, db.ForeignKey('customer.customerid'))
    chefid = db.Column(db.Integer, db.ForeignKey('chef.chefid'))
    cuisineid = db.Column(db.Integer, db.ForeignKey('cuisine.cuisineid'))
    order_date = db.Column(db.DateTime)
    req_date = db.Column(db.DateTime)
    comment = db.Column(db.String(300))

    def __init__(self, customerid, chefid, cuisineid, order_date, req_date, comment):
        self.customerid = customerid
        self.chefid = chefid
        self.cuisineid = cuisineid
        self.order_date = order_date
        self.req_date = req_date
        self.comment = comment

    def __repr__(self):
        return '<OrderID %r>' % self.orderid
# END OrderFood

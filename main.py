from flask import Flask, session, redirect, url_for, escape, request, render_template, flash, logging
from passlib.hash import sha256_crypt
from flaskext.mysql import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'aayesha163'
app.config['MYSQL_DATABASE_DB'] = 'eatin'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# app.config['MYSQL_CURSORCLASS'] = 'Dictcursor'
mysql.init_app(app)

@app.route('/')
def index():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html', session_user_name=username_session)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_form  = request.form['username']
        password_form  = request.form['password']
        cur.execute("SELECT emailid FROM user WHERE emailid = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT password FROM user WHERE emailid = %s;", [username_form]) # FETCH THE HASHED PASSWORD
            for row in cur.fetchall():
                password = password_form.encode('utf-8')
                if password_form == row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                else:
                    error = "Invalid Credential"
        else:
            error = "Invalid Credential"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

class SignupForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=50)])
    last_name = StringField('Last Name', [validators.Length(min=1, max=50)])
    email_id = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')
    usertype = StringField('User Type', [validators.Length(min=4,max=10)])
    apartment_no = StringField('Apartment No', [validators.Length(min=1, max=50)])
    street = StringField('Street', [validators.Length(min=1, max=50)])
    city = StringField('City', [validators.Length(min=1, max=50)])
    state = StringField('State', [validators.Length(min=2, max=10)])
    zipcode = StringField('Zipcode', [validators.Length(min=4, max=10)])
    country = StringField('Country', [validators.Length(min=4, max=50)])
    phone_number = StringField('Phone', [validators.Length(min=4, max=50)])
    preference = StringField('Preference', [validators.Length(min=4, max=50)])

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm(request.form)
    if (request.method == 'POST' and form.validate()):
        first_name = form.first_name.data
        last_name = form.last_name.data
        email_id = form.email_id.data
        password = sha256_crypt.encrypt(str(form.password))
        user_type = form.usertype.data
        apartment_no = form.apartment_no.data
        street = form.street.data
        city = form.city.data
        state = form.state.data
        zipcode = form.zipcode.data
        country = form.country.data
        phone_number = form.phone_number.data
        preference = form.preference.data

        # database connect
        conn = mysql.connect()

        # Create cursor
        cur = conn.cursor()

        # Execute query
        cur.execute("INSERT INTO user(emailid, password, fname, lname, user_type) VALUES(%s, %s, %s, %s, %s)",
                    (email_id, password, first_name, last_name, user_type))
        cur.execute("INSERT INTO customer (customerid, address,street,city,state,zipcode,country,phone_number,preference) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (int(cur.lastrowid), apartment_no, street, city, state, int(zipcode), country, phone_number, preference))

        conn.commit()

        cur.close()

        flash('You are now registered and login', 'success')

        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/fooditem')
def fooditem():
    return render_template('fooditem.html')


@app.route('/orderhistory')
def orderhistory():
    return render_template('orderhistory.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contactus')
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


@app.route('/cheflist', methods=['GET', 'POST'])
def cheflist():
    return render_template('cheflist.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)

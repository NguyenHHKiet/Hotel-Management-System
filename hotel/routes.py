from hotel import db, app, mysql
from .forms import AmenityForm, GuestsForm, RegisterForm, LoginForm, RoomForm
from flask import flash, redirect, render_template, request, url_for
from .models import User
from flask_login import current_user, login_user, logout_user, login_required

# routes

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')

        return redirect(url_for('home'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home"))


@app.route('/amenities')
def amenities():
    cur = mysql.connection.cursor()

    result=cur.execute("SELECT * FROM amenities")

    amenities = cur.fetchall()

    if result > 0:
        return render_template('amenities.html', amenities=amenities)
    else:
        msg = 'No facilites available currently'
        return render_template('amenities.html', msg=msg)

    cur.close()

@app.route('/rooms')
def rooms():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM rooms")

    rooms = cur.fetchall()

    if result > 0:
        return render_template('rooms.html', rooms=rooms)
    else:
        msg = 'No rooms available currently'
        return render_template('rooms.html', msg=msg)

# dashboard

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/admin_amenities')
@login_required
def admin_amenities():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM amenities")

    amenities = cur.fetchall()

    if result > 0:
        return render_template('admin_amenities.html', amenities=amenities)
    else:
        msg = 'No Facilities available'
        return render_template('dashboard.html', msg=msg)

    cur.close()
    return render_template('admin_amenities.html')

@app.route('/add_amenity', methods=['GET', 'POST'])
@login_required
def add_amenity():
    form = AmenityForm()

    if request.method == 'POST':
        print("YES")

        type = form.type.data
        status = form.status.data
        capacity = form.capacity.data
        title = form.title.data
        description = form.description.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO amenities(a_type, a_status, a_capacity, a_title, a_description) VALUES(%s, %s, %s, %s, %s)", (type, status, capacity, title, description))

        mysql.connection.commit()

        cur.close()

        flash('Facility Added Successfully', 'success')

        return redirect(url_for('admin_amenities'))
    print(form.errors)
    return render_template('add_amenity.html', form=form)


@app.route('/edit_amenity/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_amenity(id):
    print("&&&&&FFGTHTRH")
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM amenities WHERE a_id=%s", [id])
    print(result)
    amenity = cur.fetchone()
    print(amenity)
    form = AmenityForm()
    print(id)

    form.type.data = str(amenity['a_type'])
    form.status.data = str(amenity['a_status'])
    form.capacity.data = str(amenity['a_capacity'])
    form.title.data = str(amenity['a_title'])
    form.description.data  = amenity['a_description']

    if request.method == 'POST':
        type = request.form['type']
        status = request.form['status']
        capacity = request.form['capacity']
        title = request.form['title']
        description  = request.form['description']

        cur = mysql.connection.cursor()

        cur.execute("UPDATE amenities SET a_type=%s, a_status=%s, a_capacity=%s, a_title=%s, a_description=%s WHERE a_id=%s", (type, status, capacity, title, description, id))

        mysql.connection.commit()

        cur.close()

        flash('Facility Updated successfully', 'success')

        return redirect(url_for('admin_amenities'))

    print(form.errors)
    return render_template('edit_amenity.html', form=form)


@app.route('/view_amenity/<string:id>/')
def view_amenity(id):
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM amenities WHERE a_id = %s", [id])
    print(result)

    amenity = cur.fetchone()

    return render_template('view_amenity.html', amenity=amenity)

@app.route('/delete_amenity/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_amenity(id):
    cur=mysql.connection.cursor()

    cur.execute("DELETE FROM amenities WHERE a_id=%s", [id])

    mysql.connection.commit()

    cur.close()

    flash('Facility Deleted', 'success')

    return redirect(url_for('admin_amenities'))


@app.route('/admin_rooms')
@login_required
def admin_rooms():
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM rooms")

    rooms = cur.fetchall()

    if result > 0:
        return render_template('admin_rooms.html', rooms=rooms)
    else:
        flash('No Rooms available!', 'danger')
        redirect(url_for('add_room'))

    cur.close()
    return render_template('admin_rooms.html')

@app.route('/add_room', methods=['GET', 'POST'])
@login_required
def add_room():
    form = RoomForm()

    if request.method == 'POST':
        number = form.number.data
        type = form.type.data
        status = form.status.data
        capacity = form.capacity.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO rooms(r_number, r_type, r_capacity, r_status) VALUES(%s, %s, %s, %s)", (number, type, capacity, status))

        mysql.connection.commit()

        cur.close()

        flash('Room Added Successfully!', 'success')

        return redirect(url_for('admin_rooms'))

    return render_template('add_room.html', form=form)


@app.route('/edit_room/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_room(id):
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM rooms WHERE r_id=%s", [id])

    article = cur.fetchone()

    form = RoomForm()

    form.type.data = article['r_type']
    form.number.data = article['r_number']
    form.status.data = article['r_status']
    form.capacity.data = article['r_capacity']

    if request.method=='POST':
        type = request.form['type']
        number = request.form['number']
        status = request.form['status']
        capacity = request.form['capacity']

        cur = mysql.connection.cursor()

        cur.execute("UPDATE rooms SET r_type=%s, r_number=%s, r_status=%s, r_capacity=%s WHERE r_id=%s", (type, number, status, capacity, id))

        mysql.connection.commit()

        cur.close()

        flash('Room Updated successfully', 'success')

        return redirect(url_for('admin_rooms'))

    return render_template('edit_room.html', form=form, id=id)


@app.route('/delete_room/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_room(id):
    cur=mysql.connection.cursor()

    cur.execute("DELETE FROM rooms WHERE r_id=%s", [id])

    mysql.connection.commit()

    cur.close()

    flash('Facility Deleted', 'success')

    return redirect(url_for('admin_rooms'))


# admin guests
@app.route('/admin_guests')
@login_required
def admin_guests():
    
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM guests")

    guests = cur.fetchall()

    if result > 0:
        return render_template('guests.html', guests=guests)
    else:
        msg = 'No guests in the Hotel currently'
        return render_template('guests.html', msg=msg)


@app.route('/add_guests', methods=['GET', 'POST'])
@login_required
def add_guests():
    form = GuestsForm()

    if request.method == 'POST':

        status = form.status.data
        name = form.name.data
        count = form.count.data
        email = form.email.data 
        streetno = form.streetno.data
        city = form.city.data
        state = form.state.data
        country = form.country.data
        pincode = form.pincode.data

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO guests(g_status, g_name, g_count, g_email, g_streetno, g_city, g_state, g_country, g_pincode) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (status, name, count, email, streetno, city, state, country ,pincode))

        mysql.connection.commit()

        cur.close()

        flash('Guests Added Successfully!', 'success')

        return redirect(url_for('admin_guests'))

    return render_template('add_guests.html', form=form)


@app.route('/edit_guests/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_guests(id):
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM guests WHERE g_id=%s", [id])

    article = cur.fetchone()

    form = GuestsForm()

    form.status.data = article['g_status']
    form.name.data = article['g_name']
    form.count.data = article['g_count']
    form.email.data = article['g_email']
    form.streetno.data = article['g_streetno']
    form.city.data = article['g_city']
    form.state.data = article['g_state']
    form.country.data = article['g_country']

    if request.method=='POST':

        status = request.form['status']
        name = request.form['name']
        count = request.form['count']
        email = request.form['email']
        streetno = request.form['streetno']
        city= request.form['city']
        state = request.form['state']
        country = request.form['country']

        cur = mysql.connection.cursor()

        cur.execute("UPDATE guests SET g_status=%s, g_name=%s, g_count=%s, g_email=%s, g_streetno=%s, g_city=%s, g_state=%s, g_country=%s WHERE g_id=%s", (status, name, count, email, streetno, city, state, country, id))

        mysql.connection.commit()

        cur.close()

        flash('Guests Updated successfully', 'success')

        return redirect(url_for('admin_guests'))

    return render_template('edit_guests.html', form=form, id=id)


@app.route('/delete_guests/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_guests(id):
    cur=mysql.connection.cursor()

    cur.execute("DELETE FROM guests WHERE g_id=%s", [id])

    mysql.connection.commit()

    cur.close()

    flash('Deleted', 'success')

    return redirect(url_for('admin_guests'))


























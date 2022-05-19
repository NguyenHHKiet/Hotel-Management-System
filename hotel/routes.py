from flask import render_template, make_response, flash, redirect, url_for, session, request, logging
from hotel import app, mysql


# routes
@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')
    
@app.route('/amenities')
def amenities():

    cur=mysql.connection.cursor()

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



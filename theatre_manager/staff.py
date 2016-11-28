from theatre_manager import app
from flask import Flask, render_template, request, session
import mysql.connector

@app.route('/staff')
def staff():
    return render_template('staff.html')
	
@app.route('/listmovies')
def listMovies():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    query = (
        "SELECT * FROM Movie ORDER BY MovieName")
    cursor.execute(query)
    movies=cursor.fetchall()
    cnx.close()
    return render_template('listmovies.html', movies=movies)
	
@app.route("/staffmenu", methods=["POST"])	
def returnStaffMenu():
    return render_template('staff.html')	
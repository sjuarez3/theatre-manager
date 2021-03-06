from theatre_manager import app
from flask import Flask, render_template, request, session
import mysql.connector

@app.route('/staff')
def staff():
    return render_template('staff.html')
	
@app.route('/attendance')
def attendance():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    query = (
        "SELECT Attend.*, Customer.FirstName, Customer.LastName, Showing.ShowingDateTime, "
		"Movie.idMovie, Movie.MovieName FROM Attend JOIN Customer ON Attend.Customer_idCustomer = "
		"Customer.idCustomer JOIN Showing ON Attend.Showing_idShowing = Showing.idShowing JOIN Movie ON "
		"Showing.Movie_idMovie = Movie.idMovie ORDER BY Attend.Rating")
    cursor.execute(query)
    attendance=cursor.fetchall()
    cnx.close()
    return render_template('attendance.html', attendance=attendance)
	
@app.route("/staffmenu", methods=["POST"])	
def returnStaffMenu():
    return render_template('staff.html')	
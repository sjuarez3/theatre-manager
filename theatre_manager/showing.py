from theatre_manager import app
from flask import Flask, render_template, request, session
import mysql.connector
	
@app.route('/addshowing')
def addShowing():
	listshowing="false"
	deleteshowing="false"
	editshowing="false"
	addshowing="true"
	
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	
	movieQuery = ("SELECT idMovie, MovieName FROM Movie ORDER BY MovieName")
	cursor.execute(movieQuery)
	movies=cursor.fetchall()
	
	roomQuery = ("SELECT * FROM TheatreRoom ORDER BY RoomNumber")
	cursor.execute(roomQuery)
	rooms=cursor.fetchall()
	
	return render_template('showings.html', ListShowing=listshowing, DeleteShowing=deleteshowing, EditShowing=editshowing, AddShowing=addshowing, movies=movies, rooms=rooms)

@app.route('/submitshowing', methods=["POST"])
def submitShowing():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    showingQuery = ("INSERT INTO Showing (ShowingDateTime, Movie_idMovie, TheatreRoom_RoomNumber, TicketPrice)"
				   "VALUES (%s, %s, %s, %s)")
    data_showing = (request.form['ShowingDateTime'], request.form['Movie_idMovie'], request.form['TheatreRoom'], request.form['Price'])
    cursor.execute(showingQuery, data_showing)
    cnx.commit()
    cnx.close()
	
    return addShowing()
	
@app.route('/removeshowing', methods=["POST"])
def removeShowing():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	showing_id = [request.form['idShowing']]
	
	showingQuery = ("DELETE FROM Attend WHERE Showing_idShowing = %s")
	cursor.execute(showingQuery, showing_id)
    
	roomQuery = ("DELETE FROM Showing WHERE idShowing = %s")
	cursor.execute(roomQuery, showing_id)
	cnx.commit()
	cnx.close()
	
	return deleteShowing()
	
@app.route('/deleteshowing')
def deleteShowing():
	listshowing="false"
	deleteshowing="true"
	editshowing="false"
	addshowing="false"
	
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT idShowing, ShowingDateTime, Movie_idMovie, TheatreRoom_RoomNumber, FORMAT(TicketPrice,2) as TicketPrice FROM Showing ORDER BY ShowingDateTime DESC")
	cursor.execute(query)
	showings=cursor.fetchall()
	
	movieQuery = ("SELECT idMovie, MovieName FROM Movie ORDER BY MovieName")
	cursor.execute(movieQuery)
	movies=cursor.fetchall()
	cnx.close()
	
	return render_template('showings.html', ListShowing=listshowing, DeleteShowing=deleteshowing, EditShowing=editshowing, AddShowing=addshowing, showings=showings, movies=movies)

@app.route("/updateshowing", methods=["POST"])	
def updateShowing():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data_showing = (request.form['ShowingDateTime'], request.form['Movie_idMovie'], request.form['TheatreRoom'],
		request.form['Price'], request.form['idShowing'])
	print(data_showing)
	showingQuery = ("UPDATE Showing SET ShowingDateTime = %s, Movie_idMovie = %s, TheatreRoom_RoomNumber = %s, TicketPrice = %s"
						" WHERE idShowing = %s")
	
	print("Attempting: " + showingQuery)
	cursor.execute(showingQuery, data_showing)
	cnx.commit()
	cnx.close()
	
	return editShowing()

@app.route("/editshowing")
def editShowing():
	listshowing="false"
	deleteshowing="false"
	editshowing="true"
	addshowing="false"
	
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT idShowing, ShowingDateTime, Movie_idMovie, TheatreRoom_RoomNumber, FORMAT(TicketPrice,2) as TicketPrice FROM Showing ORDER BY ShowingDateTime DESC")
	cursor.execute(query)
	showings=cursor.fetchall()
	
	movieQuery = ("SELECT idMovie, MovieName FROM Movie ORDER BY MovieName")
	cursor.execute(movieQuery)
	movies=cursor.fetchall()
	
	roomQuery = ("SELECT * FROM TheatreRoom ORDER BY RoomNumber")
	cursor.execute(roomQuery)
	rooms=cursor.fetchall()
	cnx.close()
	
	return render_template('showings.html', ListShowing=listshowing, DeleteShowing=deleteshowing, EditShowing=editshowing, AddShowing=addshowing, showings=showings, movies=movies, rooms=rooms)

@app.route('/listshowings')
def listShowing():
	listshowing="true"
	deleteshowing="false"
	editshowing="false"
	addshowing="false"
	
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT idShowing, ShowingDateTime, Movie_idMovie, TheatreRoom_RoomNumber, FORMAT(TicketPrice,2) as TicketPrice FROM Showing ORDER BY ShowingDateTime DESC")
	cursor.execute(query)
	showings=cursor.fetchall()
	cnx.close()
	
	return render_template('showings.html', ListShowing=listshowing, DeleteShowing=deleteshowing, EditShowing=editshowing, AddShowing=addshowing, showings=showings)
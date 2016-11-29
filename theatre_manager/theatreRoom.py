from theatre_manager import app
from flask import Flask, render_template, request, session
import mysql.connector
	
@app.route('/addroom')
def addTheatreRoom():
	listroom="false"
	deleteroom="false"
	editroom="false"
	addroom="true"
	return render_template('theatre.html', ListRoom=listroom, DeleteRoom=deleteroom, EditRoom=editroom, AddRoom=addroom)

@app.route('/submitroom', methods=["POST"])
def submitTheatreRoom():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_room = ("INSERT INTO TheatreRoom (RoomNumber, Capacity) VALUES (%s, %s)")
    data_room = (request.form['RoomNumber'], request.form['Capacity'])
    cursor.execute(insert_room, data_room)
    cnx.commit()
    cnx.close()
	
    return addTheatreRoom()
	
@app.route('/removeroom', methods=["POST"])
def removeTheatreRoom():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	room_number = [request.form['RoomNumber']]
	
	delete_showing = ("DELETE FROM Showing WHERE TheatreRoom_RoomNumber = %s")
	cursor.execute(delete_showing, room_number)
    
	delete_room = ("DELETE FROM TheatreRoom WHERE RoomNumber = %s")
	cursor.execute(delete_room, room_number)
	cnx.commit()
	cnx.close()
	
	return deleteTheatreRoom()
	
@app.route('/deleteroom')
def deleteTheatreRoom():
	listroom="false"
	deleteroom="true"
	editroom="false"
	addroom="false"
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * FROM TheatreRoom ORDER BY RoomNumber")
	cursor.execute(query)
	rooms=cursor.fetchall()
	cnx.close()
	
	return render_template('theatre.html', ListRoom=listroom, DeleteRoom=deleteroom, EditRoom=editroom, AddRoom=addroom, rooms=rooms)

@app.route("/updateroom", methods=["POST"])	
def updateTheatreRoom():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data_room = (request.form['Capacity'], request.form['RoomNumber'])
	update_room = ("UPDATE TheatreRoom SET Capacity = %s WHERE RoomNumber = %s")
	
	print("Attempting: " + update_room)
	cursor.execute(update_room, data_room)
	cnx.commit()
	cnx.close()
	
	return editTheatreRoom()

@app.route("/editroom")
def editTheatreRoom():
	listroom="false"
	deleteroom="false"
	editroom="true"
	addroom="false"
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * FROM TheatreRoom ORDER BY RoomNumber")
	cursor.execute(query)
	rooms=cursor.fetchall()
	cnx.close()
    
	return render_template('theatre.html', ListRoom=listroom, DeleteRoom=deleteroom, EditRoom=editroom, AddRoom=addroom, rooms=rooms)

@app.route('/listroom')
def listTheatreRoom():
	listroom="true"
	deleteroom="false"
	editroom="false"
	addroom="false"
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * FROM TheatreRoom ORDER BY RoomNumber")
	cursor.execute(query)
	rooms=cursor.fetchall()
	cnx.close()
	return render_template('theatre.html', ListRoom=listroom, DeleteRoom=deleteroom, EditRoom=editroom, AddRoom=addroom, rooms=rooms)
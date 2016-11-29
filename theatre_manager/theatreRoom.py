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
	room_number = request.form['RoomNumber']
	
	delete_room = ("DELETE FROM Showing WHERE TheatreRoom_RoomNumber =" + room_number)
	cursor.execute(delete_room)
    
	delete_room = ("DELETE FROM TheatreRoom WHERE RoomNumber =" + room_number)
	cursor.execute(delete_room)
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
	roomNumber = request.form['RoomNumber']
    
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data_capacity = (request.form['Capacity'])
	update_room = ("UPDATE TheatreRoom SET Capacity =" + data_capacity + " WHERE RoomNumber = " + str(roomNumber))
	print("Attempting: " + update_room)
	cursor.execute(update_room)
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
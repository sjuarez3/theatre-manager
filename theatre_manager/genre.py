from theatre_manager import app
from flask import Flask, render_template, request, session
import mysql.connector
	
@app.route('/addgenre')
def addGenre():
	listgenre="false"
	deletegenre="false"
	editgenre="false"
	addgenre="true"
	return render_template('genre.html', ListGenre=listgenre, DeleteGenre=deletegenre, EditGenre=editgenre, AddGenre=addgenre)

@app.route('/submitgenre', methods=["POST"])
def submitGenre():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_genre = ("INSERT INTO Genre (Genre, Movie_idMovie) VALUES (%s, (SELECT idMovie FROM Movie WHERE MovieName = %s))")
    data_genre = (request.form['Genre'], request.form['MovieTitle'])
    cursor.execute(insert_genre, data_genre)
    cnx.commit()
    cnx.close()
	
    return addGenre()
	
@app.route('/removegenre', methods=["POST"])
def removeGenre():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	movie_id = request.form['MovieID']
	genre = request.form['Genre']
	
	delete_genre = ("DELETE FROM Genre WHERE Movie_idMovie =" + movie_id + " AND Genre ='" + genre +"'")
	cursor.execute(delete_genre)
    
	cnx.commit()
	cnx.close()
	
	return deleteGenre()
	
@app.route('/deletegenre')
def deleteGenre():
	listgenre="false"
	deletegenre="true"
	editgenre="false"
	addgenre="false"
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT MovieName,Genre,idMovie FROM Genre,Movie WHERE Genre.Movie_idMovie = Movie.idMovie ORDER BY MovieName")
	cursor.execute(query)
	genres=cursor.fetchall()
	cnx.close()
	
	return render_template('genre.html', ListGenre=listgenre, DeleteGenre=deletegenre, EditGenre=editgenre, AddGenre=addgenre, genres=genres)

@app.route("/updategenre", methods=["POST"])	
def updateGenre():
	genre = request.form['Genre']
    
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data_Movie = (request.form['MovieName'])
	update_genre = ("UPDATE Genre SET Genre =" + genre + " WHERE Movie_idMovie = (SELECT idMovie FROM Movie WHERE MovieName ="+ data_Movie +")")
	print("Attempting: " + update_genre)
	cursor.execute(update_room)
	cnx.commit()
	cnx.close()
	
	return editGenre()

@app.route("/editgenre")
def editGenre():
	listgenre="false"
	deletegenre="false"
	editgenre="true"
	addgenre="false"
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT MovieName,Genre,idMovie FROM Genre,Movie WHERE Genre.Movie_idMovie = Movie.idMovie ORDER BY MovieName")
	cursor.execute(query)
	genres=cursor.fetchall()
	cnx.close()
    
	return render_template('genre.html', ListGenre=listgenre, DeleteGenre=deletegenre, EditGenre=editgenre, AddGenre=addgenre, genres=genres)

@app.route('/listgenres')
def listGenre():
	listgenre="true"
	deletegenre="false"
	editgenre="false"
	addgenre="false"
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT MovieName,Genre,idMovie FROM Genre,Movie WHERE Genre.Movie_idMovie = Movie.idMovie ORDER BY MovieName")
	cursor.execute(query)
	genres=cursor.fetchall()
	cnx.close()
	return render_template('genre.html', ListGenre=listgenre, DeleteGenre=deletegenre, EditGenre=editgenre, AddGenre=addgenre, genres=genres)
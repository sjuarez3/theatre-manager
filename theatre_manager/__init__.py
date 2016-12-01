from flask import Flask, render_template, request, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "key"

import theatre_manager.staff
import theatre_manager.movie
import theatre_manager.customer
import theatre_manager.theatreRoom
import theatre_manager.genre
import theatre_manager.showing

@app.route("/")
def login():
    return render_template('login.html')
	
@app.route('/signup')
def signup():
    return render_template('signup.html')
	
@app.route('/viewprofile')
def viewProfile():
    FirstName = session.get('FirstName', None)
    LastName = session.get('LastName', None)
    EmailAddress = session.get('EmailAddress', None)
    Sex = session.get('Sex', None)
    idCustomer = session.get('idCustomer', None)
    return render_template('customerprofile.html', FirstName=FirstName, LastName=LastName, EmailAddress=EmailAddress, Sex=Sex, idCustomer=idCustomer)

@app.route('/index', methods=["POST"])
def index():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    insert_stmt = (
        "INSERT INTO Customer (FirstName, LastName, EmailAddress, Sex) "
        "VALUES (%s, %s, %s, %s)"
    )
    data = (request.form['FirstName'], request.form['LastName'], request.form['EmailAddress'], request.form['Sex'])
    cursor.execute(insert_stmt, data)
    cnx.commit()
    cnx.close()
    return render_template('index.html', FirstName=request.form['FirstName'], LastName=request.form['LastName'], EmailAddress=request.form['EmailAddress'], Sex=request.form['Sex'])

@app.route('/mainMenu', methods=["POST"])
def mainMenu():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()

    FirstName = request.form['FirstName']
    session['FirstName'] = request.form['FirstName']
    LastName = request.form['LastName']
    session['LastName'] = request.form['LastName']
    EmailAddress = request.form['EmailAddress']
    session['EmailAddress'] = request.form['EmailAddress']
	
    query = ("SELECT * FROM Customer WHERE FirstName = '" + FirstName + "' AND LastName = '" + LastName + "' AND EmailAddress = '" + EmailAddress + "'")
    cursor.execute(query)
    print("Attempting: " + query)
    customers=cursor.fetchall()
	
    for row in customers:
        idCustomer=row[0]
        session['idCustomer']=idCustomer
        Sex=row[4]
        session['Sex'] = Sex
	
    cnx.commit()
    cnx.close()
    return render_template('mainmenu.html', FirstName=request.form['FirstName'], LastName=request.form['LastName'], EmailAddress=request.form['EmailAddress'], Sex=Sex)

@app.route("/moviesWatched")
def movieSeen():
	idCustomer = session.get('idCustomer', None)
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	
	query = ("SELECT Movie.MovieName, DATE_FORMAT(Showing.ShowingDateTime, '%M-%d-%Y') AS ShowingDate, "
	         "TIME_FORMAT(Showing.ShowingDateTime,'%r') AS ShowingTime, Attend.Rating "
	         "FROM Attend, Customer, Movie, Showing " 
			 "WHERE Customer.idCustomer = Attend.Customer_idCustomer "
			 "AND Attend.Showing_idShowing = Showing.idShowing " 
			 "AND Movie.idMovie = Showing.Movie_idMovie " 
			 "AND Attend.Customer_idCustomer = " + str(idCustomer) +
			 " ORDER BY Showing.ShowingDateTime DESC")
	cursor.execute(query)
	moviesWatched=cursor.fetchall()
	cnx.close()
	return render_template('movielistseen.html' , moviesWatched=moviesWatched, FirstName=session.get('FirstName', None), LastName=session.get('LastName', None))

@app.route("/ratemovie")
def rateMovie():
	idCustomer = session.get('idCustomer', None)
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT Movie.MovieName, DATE_FORMAT(Showing.ShowingDateTime, '%M-%d-%Y') AS ShowingDate, "
	         "TIME_FORMAT(Showing.ShowingDateTime,'%r') AS ShowingTime, Attend.Rating, Showing.idShowing "
	         "FROM Attend, Customer, Movie, Showing " 
			 "WHERE Customer.idCustomer = Attend.Customer_idCustomer "
			 "AND Attend.Showing_idShowing = Showing.idShowing " 
			 "AND Movie.idMovie = Showing.Movie_idMovie " 
			 "AND Attend.Customer_idCustomer = " + str(idCustomer) + 
			 " ORDER BY Showing.ShowingDateTime DESC")
	cursor.execute(query)
	showings=cursor.fetchall()
	cnx.close()
	
	return render_template('ratemovie.html',showings=showings)

@app.route("/submitrating", methods=["POST"])	
def saveRating():
	idCustomer = str(session.get('idCustomer', None))
	idShowing = str(request.form['Showingid'])
	rating=str(request.form['Rating'])
	
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("UPDATE Attend SET Rating =" + rating +  " WHERE Customer_idCustomer =" + idCustomer + " AND Showing_idShowing =" + idShowing)

	cursor.execute(query)
	cnx.commit()
	cnx.close()
	
	return rateMovie()

@app.route("/startMenu", methods=["POST"])	
def returnStartMenu():
    return render_template('mainmenu.html', FirstName=session.get('FirstName', None), LastName=session.get('LastName', None), EmailAddress=session.get('EmailAddress', None), Sex=session.get('Sex', None))	

@app.route("/logout", methods=["POST"])	
def signOut():
	return render_template('login.html')

@app.route('/searchshowtimes')
def searchShowtimes(showings=None):
	showings=showings
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	if not showings:
		query = (
        "SELECT Showing.idShowing, DATE_FORMAT(Showing.ShowingDateTime, '%M-%d-%Y') AS ShowingDate, TIME_FORMAT(Showing.ShowingDateTime,'%r') AS ShowingTime, Showing.Movie_idMovie, Showing.TheatreRoom_RoomNumber,FORMAT(Showing.TicketPrice,2), GROUP_CONCAT(DISTINCT(Genre.Genre)) as Genre, Movie.MovieName, TheatreRoom.RoomNumber FROM Showing JOIN Genre "
		"ON Showing.Movie_idMovie = Genre.Movie_idMovie JOIN TheatreRoom ON Showing.TheatreRoom_RoomNumber "
		"= TheatreRoom.RoomNumber JOIN Movie ON Showing.Movie_idMovie = Movie.idMovie GROUP by Movie_idMovie, idShowing ORDER BY ShowingDate DESC, ShowingTime DESC")
		cursor.execute(query)
		showings=cursor.fetchall()
		
	genreQuery = ("SELECT DISTINCT Genre FROM Genre")
	cursor.execute(genreQuery)
	genres=cursor.fetchall()
	cnx.close()
	return render_template('searchshowtimes.html', showings=showings, genres=genres)
	
@app.route('/submitsearch', methods=["POST"])
def submitSearch():
	startDate = request.form['startDate']
	endDate = request.form['endDate']
	MovieName = request.form['MovieName']
	genre = request.form['genre']
	seatCapacity = request.form['seats'];
	
	AddAnd = False
	AddWhere = False
	data = []

	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = (
        "SELECT Showing.idShowing, DATE_FORMAT(Showing.ShowingDateTime, '%M-%d-%Y') AS ShowingDate, TIME_FORMAT(Showing.ShowingDateTime,'%r') AS ShowingTime, Showing.Movie_idMovie, Showing.TheatreRoom_RoomNumber, "
		"FORMAT(Showing.TicketPrice,2) as TicketPrice, GROUP_CONCAT(DISTINCT(Genre.Genre)) as Genre, Movie.MovieName, TheatreRoom.RoomNumber FROM Showing JOIN Genre "
		"ON Showing.Movie_idMovie = Genre.Movie_idMovie JOIN TheatreRoom ON Showing.TheatreRoom_RoomNumber "
		"= TheatreRoom.RoomNumber JOIN Movie ON Showing.Movie_idMovie = Movie.idMovie")
	
	if MovieName != '':
		AddAnd = True
		AddWhere = True
		query += " WHERE Movie.MovieName = %s "
		data.append(MovieName)
	
	if startDate != '':
		if AddAnd:
			query += "AND"
		if not AddWhere:
			query += " WHERE"
		AddWhere = True
		AddAnd = True
		query += " Showing.ShowingDateTime > %s "
		data.append(startDate)
	
	if endDate != '':
		if AddAnd:
			query += "AND"
		if not AddWhere:
			query += " WHERE"
		AddWhere = True
		AddAnd = True
		query += " Showing.ShowingDateTime < %s "
		data.append(endDate)
	
	if genre != '':
		if AddAnd:
			query += "AND"
		if not AddWhere:
			query += " WHERE"
		AddWhere = True
		AddAnd = True
		query += " Genre.Genre = %s "
		data.append(genre)
	
	if seatCapacity != "false":
		if AddAnd:
			query += "AND"
		if not AddWhere:
			query += " WHERE"
		query += (" Showing.idShowing in (SELECT IF((TheatreRoom.Capacity - COUNT(Attend.Showing_idShowing)),Attend.Showing_idShowing, '') AS idShowing " 
				  "FROM Attend,Showing,TheatreRoom "
				  "WHERE TheatreRoom.RoomNumber = Showing.TheatreRoom_RoomNumber AND Attend.Showing_idShowing = Showing.idShowing GROUP BY Attend.Showing_idShowing)"
				  " OR Showing.idShowing not in (SELECT Showing_idShowing FROM Attend)")
	
	query += " GROUP by Movie_idMovie, idShowing ORDER BY ShowingDate DESC, ShowingTime DESC"	
	
	if len(data) == 0:
		cursor.execute(query)
	else:
		cursor.execute(query,data)
	showings=cursor.fetchall()
	cnx.close()
	return searchShowtimes(showings)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
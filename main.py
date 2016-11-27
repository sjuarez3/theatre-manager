from flask import Flask, render_template, request, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "super secret key"

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
	
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
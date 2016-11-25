from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

@app.route("/")
def login():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    query = ("SELECT * FROM Customer")
    cursor.execute(query)
    customers=cursor.fetchall()
    cnx.close()
    return render_template('customers.html', customers=customers)
	
@app.route('/entercustomer')
def addCustomer(name=None):
    return render_template('form6.html', name=name)

@app.route('/submit', methods=["POST"])
def submit():
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
    return render_template('index.html', firstname=request.form['FirstName'], lastname=request.form['LastName'], EmailAddress=request.form['EmailAddress'], Sex=request.form['Sex'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
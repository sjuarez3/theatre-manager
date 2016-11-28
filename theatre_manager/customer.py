from theatre_manager import app
from flask import Flask, render_template, request, session
import mysql.connector

@app.route('/listcustomers')
def listCustomers():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    query = (
        "SELECT * FROM Customer ORDER BY LastName")
    cursor.execute(query)
    customers=cursor.fetchall()
    cnx.close()
    return render_template('listcustomers.html', customers=customers)
	
@app.route('/addcustomer')
def addCustomer():
    return render_template('addcustomer.html')

@app.route('/submitcustomer', methods=["POST"])
def submitCustomer():
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
	
    return addCustomer()
	
@app.route('/deletecustomer')
def deleteCustomer():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    query = ("SELECT * FROM Customer ORDER BY LastName")
    cursor.execute(query)
    customers=cursor.fetchall()
    cnx.close()
	
    return render_template('deletecustomer.html', customers=customers)

@app.route('/removecustomer', methods=["POST"])
def removeCustomer():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    delete_stmt = (
    "DELETE FROM Customer WHERE FirstName = %s AND LastName = %s AND EmailAddress = %s ")
    data = (request.form['FirstName'], request.form['LastName'], request.form['EmailAddress'])
    cursor.execute(delete_stmt, data)
    cnx.commit()
    cnx.close()
	
    return deleteCustomer()
	
@app.route("/editcustomer")
def editCustomer():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    query = ("SELECT * FROM Customer ORDER BY LastName" )
    cursor.execute(query)
    customers=cursor.fetchall()
    cnx.close()
    
    return render_template('editcustomer.html', customers=customers)

@app.route("/updatecustomer", methods=["POST"])	
def updateCustomer():
    idCustomer = request.form['idCustomer']
    
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    update_stmt = (
        "UPDATE Customer SET FirstName = %s, LastName = %s, EmailAddress = %s, Sex = %s WHERE idCustomer = " + str(idCustomer) + "")
    data = (request.form['FirstName'], request.form['LastName'], request.form['EmailAddress'], request.form['Sex'])
    print("Attempting: " + update_stmt)
    cursor.execute(update_stmt, data)
    cnx.commit()
    cnx.close()
	
    return editCustomer()
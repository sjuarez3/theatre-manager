from theatre_manager import app
from flask import Flask, render_template, request, session
import mysql.connector

@app.route('/staff')
def staff():
    return render_template('staff.html')


from flask import Flask, render_template,request,jsonify
import requests
import pyodbc

app = Flask(__name__)

result1=0
result20=0
result3=0

@app.route("/")
def index():
	#Import Libraries
	return render_template('index.html')

@app.route("/temp")
def temperature():
	global result1
	server = 'virutal.database.windows.net' 
	database = 'COVID19-db' 
	username = 'Ismiledb' 
	password = 'Ismile@123' 
	cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()
	cursor.execute("SELECT TOP 1 * FROM SensorDetails ORDER BY Personid DESC")
	row=cursor.fetchone()
	print("--------------------------database connectivity-----------")
	print("fetched temperature:"+str(row[2]))
	result1 = 0 if 96.6<= row[2] <=99.6 else 1
	print("result  "+str(result1))
	return render_template('Pulse_rate.html')
	
@app.route("/Pulse ")
def Pulse_rate():
	server = 'virutal.database.windows.net' 
	database = 'COVID19-db' 
	username = 'Ismiledb'  
	password = 'Ismile@123' 
	cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
	cursor = cnxn.cursor()
	cursor.execute("SELECT TOP 1 * FROM SensorDetails ORDER BY Personid DESC")
	row=cursor.fetchone()
	print("--------------------------database connectivity-----------")
	print("Pulse_rate   "+str(row[3]))
	print("oxymeter  "+str(row[4]))
	result2 = 0 if  row[3] >=60 else 1
	result3 = 1 if  row[4] >=80 else 0
	print("result   "+str(result1))
	print("result   "+str(result2))
	print("result   "+str(result3))
	Personid=13
	cursor.execute("INSERT INTO HealthResult(Personid,Temperataure,PulseRate,Oximeter) VALUES (?,?,?,?)",(Personid,result1,result2,result3))
	cnxn.commit()

	return render_template('results.html',result1=result1,result2=result2,result3=result3)



if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask
from flaskext.mysql import MySQL
 
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'culturp7_eric'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mysqlhm'
app.config['MYSQL_DATABASE_DB'] = 'culturp7_ktc'
app.config['MYSQL_DATABASE_HOST'] = '50.116.65.175'
mysql.init_app(app)
 
@app.route("/")
def hello():
	cursor = mysql.connect().cursor()
	cursor.execute("SHOW TABLES")
	tablenames = cursor.fetchall()
	print type(tablenames)
	print tablenames
	return "Welcome to Python Flask App!"

if __name__ == "__main__":
    app.run()

# WHOOOOO :)
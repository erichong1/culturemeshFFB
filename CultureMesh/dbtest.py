from flask import Flask, render_template
from flaskext.mysql import MySQL
app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'culturp7_eric'
app.config['MYSQL_DATABASE_PASSWORD'] = 'culturemesh1'
app.config['MYSQL_DATABASE_DB'] = 'culturp7_ktc'
app.config['MYSQL_DATABASE_HOST'] = '50.116.65.175'
mysql.init_app(app)

@app.route("/")
def home():
	cursor = mysql.connect().cursor()
	cursor.execute("SHOW TABLES")
	tablenames = cursor.fetchall()
	return str(tablenames)

if __name__ == "__main__":
	app.run()
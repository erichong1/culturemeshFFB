from flask import Flask, render_template, request
app = Flask(__name__)

from flaskext.mysql import MySQL 
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'culturp7_eric'
app.config['MYSQL_DATABASE_PASSWORD'] = 'mysqlhm'
app.config['MYSQL_DATABASE_DB'] = 'culturp7_ktc'
app.config['MYSQL_DATABASE_HOST'] = '50.116.65.175'
mysql.init_app(app)

visitors = 0

@app.route("/count")
def hello():
	global visitors
	visitors += 1
	return str(visitors)

@app.route("/about")
def about():
	return "<img src='https://s30.postimg.org/958ms8rip/Screen_Shot_2016_12_07_at_5_46_23_PM.png' height='500px'></img>dwefoie</title><b>HAHHAHHHH</b>"

@app.route("/syriatosanfrancisco")
def get():
	#return connecttodatabase("syria sanfrancisco")
	cursor = mysql.connect().cursor()
	cursor.execute("SHOW TABLES")
	tablenames = cursor.fetchall()
	return "tablenames: " + str(tablenames)

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/search")
def search():
	from_location = request.args.get("from")
	in_location = request.args.get("in")
	return from_location + in_location

@app.route("/retrieve_tables_and_columns")
def retrieve_tables_and_columns():
	cursor = mysql.connect().cursor()
	cursor.execute("SHOW TABLES")
	tablenames = cursor.fetchall()
	complete_list = ""
	for i in xrange(len(tablenames)):
		cur_table = str(tablenames[i]).split("'")[1]
		complete_list += cur_table
		complete_list += ": "
		#cursor = mysql.connect().cursor()
		cursor.execute("DESCRIBE " + cur_table)
		cur_table_columns = cursor.fetchall()
		for j in cur_table_columns:
			complete_list += str(j[0]) + ", "
		complete_list += "<br \\><br \\>"
	return complete_list

@app.route("/select_users")
def select_users():
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT id, username, first_name, last_name FROM users")
	users = cursor.fetchall()
	s = ""
	for u in users:
		s += str(u) + "<br \\>"
	return s

def retrieve(from_location, in_location):
	pass



if __name__ == "__main__":
	app.run()
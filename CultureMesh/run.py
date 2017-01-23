from flask import Flask, render_template, request
from flaskext.mysql import MySQL 
app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'culturp7_eric'
app.config['MYSQL_DATABASE_PASSWORD'] = 'culturemesh17'
app.config['MYSQL_DATABASE_DB'] = 'culturp7_rehearsal'
app.config['MYSQL_DATABASE_HOST'] = '50.116.65.175'
mysql.init_app(app)

visitors = 0

# from dbroutes import db_api
# app.register_blueprint(db_api)

@app.route("/count")
def hello():
	global visitors
	visitors += 1
	return str(visitors)

@app.route("/about")
def about():
	return "<img src='https://s30.postimg.org/958ms8rip/Screen_Shot_2016_12_07_at_5_46_23_PM.png' height='500px'></img>dwefoie</title><b>HAHHAHHHH</b>"

@app.route("/showtables")
def get():
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
	print 1
	cursor = mysql.connect().cursor()
	print 2
	cursor.execute('select population, region_name, country_name from cities where name="' + from_location + '"')
	print 3
	from_info = cursor.fetchall()
	print 4
	cursor.execute('select population, region_name, country_name from cities where name="' + in_location + '"')
	print 5
	in_info = cursor.fetchall()
	print 6
	return from_location + ": " + str(from_info) + "<br>" + in_location + ": " + str(in_info)

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

@app.route("/sql")
def sql():
	cursor = mysql.connect().cursor()
	cmd = request.args.get("command")
	if cmd != None:
		cursor.execute(cmd) 
		return str(cursor.fetchall()) + '<br><br><form action="sql"><input type="text" name="command" placeholder="SQL command"></input></form>'
	else:
		return '<form action="sql"><input type="text" name="command" placeholder="SQL command"></input></form>'

def retrieve(from_location, in_location):
	pass



if __name__ == "__main__":
	app.run()
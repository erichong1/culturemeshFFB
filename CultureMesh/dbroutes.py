from flask import Blueprint

db_api = Blueprint("db_api", __name__)

@db_api.route("/retrieve_tables_and_columns")
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

@db_api.route("/select_users")
def select_users():
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT id, username, first_name, last_name FROM users")
	users = cursor.fetchall()
	s = ""
	for u in users:
		s += str(u) + "<br \\>"
	return s
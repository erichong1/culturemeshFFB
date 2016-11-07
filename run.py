from flask import Flask, render_template
app = Flask(__name__)

visitors = 0

@app.route("/")
def hello():
	global visitors
	visitors += 1
	return str(visitors)

@app.route("/about")
def about():
	return "<b>HAHHAHHHH</b>"

@app.route("/syriatosanfrancisco")
def get():
	return connecttodatabase("syria sanfrancisco")

if __name__ == "__main__":
	app.run()
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
def main():
	return render_template('index.html')

@app.route("/playerNames/", methods=['POST'])
def playerOne():
	pOneName = request.form['playerOneName']
	pTwoName = request.form['playerTwoName']
	return redirect('/')

if __name__ == "__main__":
	app.debug = True
	app.run()
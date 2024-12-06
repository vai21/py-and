from flask import Flask, render_template
from tasks import connect_to_bluetooth, connect_to_cable

app = Flask(__name__)



@app.route("/")
def control():
    return render_template('control.html')

@app.route("/bluetooth")
def bluetooth():
    connect_to_bluetooth.delay()
    return "<a href='/'> Back to Home</a> <br>Running bluetooth connection"

@app.route("/cable")
def cable():
    connect_to_cable.delay()
    return "<a href='/'> Back to Home</a> <br>Running cable connection"


if __name__ == '__main__':
    app.run(debug=True)


from helpers import trigger_run_bluetooth, run_serial
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def control():
    return render_template('control.html')

@app.route("/bluetooth")
def bluetooth():
    message = trigger_run_bluetooth()
    if (message):
        # message += "<a href='/'> Back to Home</a> <br>"
        return message
    return 'Running bluetooth connection'
@app.route("/cable")
def cable():
    message = run_serial()
    if (message):
        message += "<a href='/'> Back to Home</a> <br>"
        return message
    return 'Running cable connection'


if __name__ == '__main__':
    app.run(debug=True)


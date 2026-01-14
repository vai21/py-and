from flask import Flask, render_template
from tasks import connect_to_bluetooth, connect_to_cable
from waitress import serve

app = Flask(__name__)



@app.route("/")
def control():
    return render_template('control.html')

@app.route("/bluetooth")
def bluetooth():
    message = connect_to_bluetooth.delay()
    print(f"response message: {message}")
    return f"<a href='/'> Back to Home</a> \
            <br>Running bluetooth connection<br> \
            <a rel='noopener' href='http://localhost:5555/task/{message}' target='_blank'> Status </a>"

@app.route("/cable")
def cable():
    message = connect_to_cable.delay()
    print(f"response message: {message}")
    return f"<a href='/'> Back to Home</a> \
            <br>Running cable connection \
            <a rel='noopener' href='http://localhost:5555/task/{message}' target='_blank'> Status </a>"


if __name__ == '__main__':
    message = connect_to_cable.delay()
    print(f"response message: {message}")
    # app.run(debug=True)
    serve(app, host='127.0.0.1', port=5000)

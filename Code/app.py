from flask import Flask, redirect, session, request, url_for
from curtain import open_curtain, close_curtain, stop_curtain, get_state
from datetime import datetime, date
from sunset_api import APIResponse
import time
import threading
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
import logging

app = Flask(__name__)

mode = "AUTO"

logging.basicConfig(
    filename = 'curtain.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)


def scheduler():
    last_data_fetch_time = None

    while True:
        today = date.today()

        if today != last_data_fetch_time:
            data = APIResponse()
            last_data_fetch_time = today
            sunrise_time = datetime.fromisoformat(data['sunrise'])
            sunset_time = datetime.fromisoformat(data['sunset'])

        if mode == "AUTO":
            current_time = datetime.now(sunrise_time.tzinfo)
            if current_time >= sunrise_time and current_time < sunset_time:
                open_curtain()
            else:
                close_curtain()
        time.sleep(120)


app.secret_key = ""
password_hash = ""

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Strict'
)

limiter = Limiter(get_remote_address, app=app, default_limits=["30 per minute"])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if check_password_hash(password_hash, request.form['password']):
            session['logged_in'] = True
            logging.info(f"Successful login from IP: {request.remote_addr}")
            return redirect(url_for('home_page'))
        else:
            logging.warning(f"Failed login attempt from IP: {request.remote_addr}")
            return 'Invalid password', 401
    return '''
            <form method="post">
                <p><input type=password name=password>
                <p><input type=submit value=Login>
            </form>
        '''


def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
@require_login
def home_page():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="5">
    <style>

    body {
        font-family: sans-serif;
        text-align: center;
        background: #1a1a2e;
        color: white;
    }

    .background_card {
        background: #16213e;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
        text-align: center;
    }

    h1 {
        font-size: 22px;
        margin-bottom: 6px;
    }

    p {
    color: #8a8aa0;
    margin-bottom: 30px;
    }

    button {
    width: 220px;
    background: #4b6cb7;
    color: white;
    border: none;
    padding: 16px;
    font-size: 16px;
    font-weight: bold;
    border-radius: 10px;
    margin: 8px;
    transition: 0.3s;
    cursor: pointer;
    }

    .buttons { display: flex; flex-direction: column; gap: 14px; }
    .open { background: #2ecc71; }
    .close { background: #fdaa48; }
    .stop { background: #ff0000; }

    button:hover {
        opacity: 0.8;
    }
    button:active {
        transform: scale(0.98);
    }

    </style>
    </head>
    <body>

        <div class="background_card">
            <h1>Welcome to the Curtain Control Server</h1>
            <p>Click on the following buttons to control the curtains:</p>
            <p>Current Mode: placeholder</p>
            <p>Curtain Status: state</p>
            <div class= "buttons">
                <a href="/open"><button class="open">Open Curtain</button></a>
                <a href="/close"><button class="close">Close Curtain</button></a>
                <a href="/stop"><button class="stop">Stop Curtain</button></a>
                <a href="/auto"><button>Return to Automatic Mode</button></a>
            </div>
        </div>
    </body>
    </html>
    """
    html = html.replace("placeholder", mode)
    html = html.replace("state", get_state())
    return html


@app.route("/open")
@require_login
def open_curtain_route():
    global mode
    mode = "MANUAL"
    logging.info(f"Curtain opened manually from IP: {request.remote_addr}")
    open_curtain()
    return redirect("/")


@app.route("/close")
@require_login
def close_curtain_route():
    global mode
    mode = "MANUAL"
    logging.info(f"Curtain closed manually from IP: {request.remote_addr}")
    close_curtain()
    return redirect("/")


@app.route("/stop")
@require_login
def stop_curtain_route():
    global mode
    mode = "MANUAL"
    logging.info(f"Curtain stopped manually from IP: {request.remote_addr}")
    stop_curtain()
    return redirect("/")


@app.route("/auto")
@require_login
def auto_mode():
    global mode
    mode = "AUTO"
    logging.info(f"Switched to automatic mode from IP: {request.remote_addr}")
    return redirect("/")


@app.route("/manual")
@require_login
def manual_mode():
    global mode
    mode = "MANUAL"
    logging.info(f"Switched to manual mode from IP: {request.remote_addr}")
    return redirect("/")


if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=scheduler, daemon=True)
    scheduler_thread.start()
    app.run(host="0.0.0.0", port=5000, ssl_context=("server.crt", "server.key"))



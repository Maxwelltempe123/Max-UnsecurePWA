from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
import user_management as dbHandler
from validate_and_sanitise import sanitise
from validate_and_sanitise import validate_password


# Code snippet for logging a message
# app.logger.critical("message")

app = Flask(__name__)

@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        feedback = request.form.get("feedback", "")
        sanitized_feedback = sanitise(feedback)
        dbHandler.insertFeedback(sanitized_feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    else:
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")

@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        DoB = request.form["dob"]
        password = vs.validate_password(password)
        dbHandler.insertUser(username, password, DoB)
        return render_template("/signup.html", state=True)
    else:
        return render_template("/signup.html")


@app.route("/index.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        isLoggedIn = dbHandler.retrieveUsers(username, password)
        if isLoggedIn:
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")

@app.route('/index.html', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def twofa():
    user_secret = pyotp.random_base32()
    totp = pyotp.TOTP(user_secret)
    totp = pyotp.TOTP(user_secret)
    otp_uri = totp.provisioning_uri(name=username,issuer_name="YourAppName")
    qr_code = pyqrcode.create(otp_uri)
    stream = BytesIO()
    qr_code.png(stream, scale=5)
    qr_code_b64 = base64.b64encode(stream.getvalue()).decode('utf-8')
    otp_input = request.form['otp']
    if request.method == 'POST':
        otp_input = request.form['otp']
        if totp.verify(otp_input):
            return render_template('success.html')
            #return redirect(url_for('home'))  # Redirect to home if OTP is valid
        else:
            return "Invalid OTP. Please try again.", 401

    return render_template('index.html')

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=5000)

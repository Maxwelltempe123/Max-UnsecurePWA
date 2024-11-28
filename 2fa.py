from flask import Flask, render_template, request, redirect, url_for, session
import userManagement as dbHandler
import pyotp
import pyqrcode
import os
import base64
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'my_secret_key'

def tw():
    user_secret = pyotp.random_base32() #generate the one-time passcode
    return redirect(url_for('enable_2fa')) #redirect to 2FA page
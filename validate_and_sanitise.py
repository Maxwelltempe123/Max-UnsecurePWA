from flask import current_app as app
import re

# Code snippet for logging a message
# app.logger.critical("message")

def sanitise(input_string):
    clean_string = re.sub(r'<.*?>', '', input_string)
    clean_string = re.escape(clean_string)
    return clean_string

def validate_password(password):
    if not issubclass(type(password), str):
        return False
    if len(password) < 8:
        return False
    if len(password) > 13:
        return False
    if re.search(r"[ ]", password):
        return False
    if not password.isalpha():
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[@$!%*?&]", password):
        return False
    if not re.findall(r"[A-Za-z]", password) < 4:
        return False
    if not re.findall(r"[0-9]", password) < 3:
        return False
    return True
from flask import current_app as app
import html
import os
import re

# Code snippet for logging a message
# app.logger.critical("message")

def sanitise(feedback):
    sanitized_feedback = html.escape(feedback)
    log_feedback(sanitized_feedback)
    return sanitized_feedback

def log_feedback(feedback):
    log_file = "feedback_log.txt"
    try:
        with open(log_file, "a") as file:
            file.write(f"{feedback}\n")
    except Exception as e:
        print(f"Error logging feedback: {e}")

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
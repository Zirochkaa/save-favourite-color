from flask import Flask

app = Flask(__name__)
app.secret_key = "anythingilike"

from app import views

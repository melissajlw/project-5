from flask import render_template
from config import app

from models.models import *
from routes.routes import *

@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")

if __name__ == "__main__":
  app.run(port=5555, debug=True)
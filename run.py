from flask import Flask, render_template, request, redirect
# Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
# Models
from models.models import db, ma
from models.models import *

# APIs
from api.conversation_api import ConversationAPI
from prometheus_flask_exporter import PrometheusMetrics

import os

print("Running...", flush=True)

app = Flask(__name__)
api = Api(app)
metrics = PrometheusMetrics(app)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False
app.config["DEBUG"] = True

# Database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db_env = os.environ.get("DB_PATH")
print(db_env)
db_uri = db_env
print("Database uri: ", flush=True)
print(db_uri, flush=True)



engine = create_engine(db_uri)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

db.init_app(app)
ma.init_app(app)


# APIs
api.add_resource(ConversationAPI,"/conversations", "/conversations")


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8082, debug=True, use_reloader=False)
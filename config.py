import os
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

project_dir = os.path.abspath(os.path.dirname(__file__))
connexion_app = connexion.App(__name__, specification_dir=project_dir)
database_file = "sqlite:///" + os.path.join(project_dir, "database.db")

#The app instance
app = connexion_app.app
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# The SqlAlchemy db instance
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)
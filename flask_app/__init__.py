from flask import Flask # type: ignore
from flask_bcrypt import Bcrypt
app = Flask(__name__)
app.secret_key = " Gforcebabyface8956"

bcrypt = Bcrypt(app)
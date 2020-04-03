from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from env import DATABASE_URI

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

CORS(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    message = db.Column(db.String())

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message

class ContactSchema(ma.Schema):
    class Meta:
        fields = ('name', 'email', 'message', 'id')

contact_schema = ContactSchema()
contact_schema = ContactSchema(many=True)

@app.route("/contact/post", methods=["POST"])
def create_contact():
    post_data = request.get_json()
    name = post_data.get("name")
    email = post_data.get("email")
    message = post_data.get("message")

    record = Contact(name, email, message)
    db.session.add(record)
    db.session.commit()

    return jsonify("Data Posted")

@app.route("/contact/get", methods=["GET"])
def get_all_contacts():
    all_contacts = Contact.query.all()
    result = contact_schema.dump(all_contacts)
    return jsonify(result)

@app.route("/contact/<id>", methods=["GET"])
def get_contact(id):
    contact = Contact.query.get(id)
    return contact_schema.jsonify(contact)


if __name__ == "__main__":
    app.debug = True
    app.run()

    
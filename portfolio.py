
from flask import Flask, render_template, request, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your_email@gmail.com'  # Your email address
app.config['MAIL_PASSWORD'] = 'your_password'  # Your email password

db = SQLAlchemy(app)
mail = Mail(app)

class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

db.create_all()

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/', methods=['GET', 'POST'])
def contact_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']

        new_data = UserData(name=name, email=email, phone=phone, subject=subject, message=message)
        db.session.add(new_data)
        db.session.commit()

        send_email(subject, message, email)

        flash('Message sent successfully!', 'success')

    return render_template('contact_form.html')

def send_email(subject, message, sender_email):
    msg = Message(subject=subject, sender=sender_email, recipients=['abhi797.abhay@gmail.com'])  # Your email address
    msg.body = message
    mail.send(msg)


if __name__=='__main__':
    app.run()

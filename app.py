# from flask import Flask, render_template, request
# from flask_sqlalchemy import SQLAlchemy
# import json
# from flask_mail import Mail

# with open ('parmas.json','r') as c:
#     parmas=json.load(c)["parmas"]
# local_server=True
# app = Flask(__name__, static_folder='statics')

# app.config.update(
#     MAIL_SERVER="smtp.gmail.com",
#     MAIL_PORT=465,  
#     MAIL_USE_SSL=True,
#     MAIL_USERNAME=parmas['user_name'],
#     MAIL_PASSWORD=parmas['password']
# )

# mail=Mail(app)


# if(local_server):
#   app.config['SQLALCHEMY_DATABASE_URI'] =parmas['local_url']
#   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = parmas['prod_url']

# db = SQLAlchemy(app)


# class Contact(db.Model):
#     s_no = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(20), nullable=True)
#     email= db.Column(db.String(30), nullable=True)
#     subject = db.Column(db.String(200), nullable=True)
#     message = db.Column(db.String(12), nullable=True)

# @app.route("/")
# def home():
#     return render_template('/index.html')   

# @app.route("/profile")
# def profile():
#     return render_template('/profile.html')   
 
# @app.route("/contact", methods=['GET', 'POST'])
# def contact():
#     if request.method == 'POST':
#         name = request.form.get('name')
#         email = request.form.get('email')
#         subject= request.form.get('subject')
#         message = request.form.get('message')


#         entry = Contact(name=name, email=email, subject=subject, message=message)
#         db.session.add(entry)
#         db.session.commit()
#         try:
#            mail.send_message ('New message from '+ name,
#                            sender=parmas['user_name'],recipients=
#                            [parmas['user_name']],
#                            body=f"Name={name}\n Email={email}\n Subject={subject}\n message={message}\n")
#            mail.send_message('thankyou for the contacting us',
#                              sender=parmas['user_name'],
#                              recipients=[email],
#                              cc=[parmas['user_name']],
#                              body=f"Dear {name},\n\nThank you for reaching out to us. We have received your message:\n"
#                                   f"\n{subject}\n\nWe will get back to you soon!\n\nBest Regards,\nYour Website Team"
#                              )
#            print("Email send sucessfully!")
#         except Exception as e:
#             print(f"Error sending emaill:{e}")

#     return render_template('index.html',parmas=parmas)
# if __name__=='__main__':
#     app.run(debug=True,port=8060)
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
import pymysql

# Use pymysql instead of MySQLdb
pymysql.install_as_MySQLdb()

# Load config
with open('parmas.json', 'r') as c:
    params = json.load(c)["parmas"]

# Flask app initialization
app = Flask(__name__, static_folder='statics')

# Email configuration
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['user_name'],
    MAIL_PASSWORD=params['password']
)
mail = Mail(app)

# Database configuration
local_server = False  # Set False for production
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_url']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# -----------------------
# Database Models
# -----------------------
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)

# -----------------------
# Routes
# -----------------------

@app.route("/")
def home():
    return render_template("index.html", parmas=params)

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        try:
            # Save to database
            entry = Contact(name=name, email=email, subject=subject, message=message)
            db.session.add(entry)
            db.session.commit()

            # Send admin email
            mail.send_message(
                subject=f'New message from {name}',
                sender=params['user_name'],
                recipients=[params['user_name']],
                body=f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\n{message}"
            )

            # Send user confirmation email
            mail.send_message(
                subject='Thank you for contacting us',
                sender=params['user_name'],
                recipients=[email],
                body=f"Dear {name},\n\nThanks for contacting us.\n\nSubject: {subject}\nMessage: {message}\n\nWe’ll get back to you soon.\n\n– Team"
            )

            print("✅ Email sent and data saved.")

        except Exception as e:
            print(f"❌ Error: {e}")

    return render_template("index.html", parmas=params)

# -----------------------
# Run the app
# -----------------------
if __name__ == "__main__":
    app.run(debug=True, port=8060)


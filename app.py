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
    parmas = json.load(c)["parmas"]

# Set this to False when using Railway (production)
local_server = False

# Initialize Flask app
app = Flask(__name__, static_folder='statics')

# Email Configuration
app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=parmas['user_name'],
    MAIL_PASSWORD=parmas['password']
)
mail = Mail(app)

# Database Configuration
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = parmas['local_url']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = parmas['prod_url']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ============================
# Database Model
# ============================
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.VARCHAR(20), nullable=True)
    subject = db.Column(db.String(255), nullable=True)
    message = db.Column(db.Text, nullable=True)

# ============================
# Routes
# ============================

@app.route("/")
def home():
    return render_template("index.html", parmas=parmas)

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        # Save to Database
        entry = Contact(name=name, email=email, subject=subject, message=message)
        db.session.add(entry)
        db.session.commit()

        # Send confirmation emails
        try:
            # To admin
            mail.send_message(
                f'New message from {name}',
                sender=parmas['user_name'],
                recipients=[parmas['user_name']],
                body=f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\n{message}"
            )
            # To user
            mail.send_message(
                'Thank you for contacting us',
                sender=parmas['user_name'],
                recipients=[email],
                cc=[parmas['user_name']],
                body=f"Dear {name},\n\nThank you for reaching out!\n\nYour message:\n{subject}\n\n{message}\n\nWe'll reply soon.\n\n– Your Website Team"
            )
            print("✅ Email sent successfully")
        except Exception as e:
            print(f"❌ Error sending email: {e}")

    return render_template("index.html", parmas=parmas)

# ============================
# Run App
# ============================
if __name__ == "__main__":
    app.run(debug=True, port=8060)

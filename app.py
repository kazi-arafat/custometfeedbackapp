from flask import Flask,flash,render_template,request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_email

app = Flask(__name__)
ENV = "dev"

if (ENV == "dev"):
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc123@localhost/CustomerFeedback'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qhgxgzgfmalnxu:a2bc34670c77162e732c08c4404918b33e7ce9096d07be2ec3710bef10bd2541@ec2-107-20-239-47.compute-1.amazonaws.com:5432/d4603d4b6h369v'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class FeedbackForm(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self,customer,dealer,rating,comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

    

@app.route("/")
def Index():
    return render_template("index.html")

@app.route("/submit",methods=['POST'])
def Submit():
    if (request.method == "POST"):
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        # print ("{0} {1} {2} {3}".format(customer,dealer,rating,comments))
        if (customer == "" or dealer == ""):
            return render_template("index.html",message="Please enter required fields.")
        # Check if the customer already submitted feedback and then proceed with further steps
        if (db.session.query(FeedbackForm).filter(FeedbackForm.customer == customer).count() == 0):
            data = FeedbackForm(customer,dealer,rating,comments)
            db.session.add(data)
            db.session.commit()
            send_email(customer, dealer, rating, comments)
            return render_template("success.html")
        return render_template("index.html",message="You have already submitted feedback.")

if (__name__ == "__main__"):
    app.run()
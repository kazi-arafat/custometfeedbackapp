import smtplib
from email.mime.text import MIMEText

def send_email(customer, dealer, rating, comments):
    port = 587
    userid = "40dc44b7a3fe59"
    pwd = "b7183feda5fb84"
    host = "smtp.mailtrap.io"

    to_email = "arafatkazi2448@gmail.com"
    from_email = "noReply@example.com"

    mail_body = f"<h3>Customer Feedback</h3><hr><ul><li>Customer Name : {customer}</li><li>Dealer Name : {dealer}</li><li>Rating : {rating}</li><li>Comments : {comments}</li></ul>"

    msg = MIMEText(mail_body,'html')
    msg['Subject'] = "Customer Feedback"
    msg['From'] = from_email
    msg['To'] = to_email

    # Send Email
    with smtplib.SMTP(host=host,port=port) as smtpServer:
        smtpServer.login(userid,pwd)
        smtpServer.sendmail(to_email, from_email, msg.as_string())
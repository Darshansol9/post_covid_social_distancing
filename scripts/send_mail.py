import email, smtplib, ssl
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



def mailMe(location,mail_id):
    
    subject = "Entry Permit"
    body = f"Hi person_name, \n\n Your request to entry at the location {location} has been accepted.\n Please use the below QR code to Code to be scanned at the entrance of the building" #Add lat long here from #add time 
    sender_email = "enter the organization mail"
    receiver_email = mail_id

    f = open('password.txt','r')
    read_password = f.readlines()[0]
    password = str(read_password).rstrip()
    
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = os.path.join(os.getcwd(),f'OnDemand_qrCode/{mail_id}.png')  # In same directory as script

    # Open PDF file in binary mode

    with open(filename, "rb") as attachment:
        #Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

    print('Please Check your Inbox')

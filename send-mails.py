import pandas as pd
import os
import smtplib
from email.message import EmailMessage

df = pd.read_csv('sending.csv')

# https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development
# https://medium.com/@rinu.gour123/python-send-email-via-smtp-ad2d259d7240
# https://stackoverflow.com/questions/6355456/starttls-extension-not-supported-by-server/41673329
# https://stackoverflow.com/questions/16512592/login-credentials-not-working-with-gmail-smtp
# https://stackoverflow.com/questions/38134714/starttls-extension-not-supported-by-server-getting-this-error-when-trying-to-s



def filterWhereEmailsNotSend(dataframe):
    return dataframe[dataframe['sentAt'].isnull()]

def updateCsvRow(dataframe, index):
    dataframe.set_value(index,'sentAt', 'cock')

def createEmailMessage(email ):
    msg = EmailMessage()
    msg['Subject'] = 'TEST MAIL'
    msg['From'] = 'your.gmail@gmail.com'
    msg['To'] = ['your.gmail@gmail.com']
    msg.set_content('This is a plain text email as a fallback')
    msg.add_alternative("""\
    <!DOCTYPE html>
    <html>
        <body>
            <h1 style="color:SlateGray;">This is an HTML EMAIL!</h1>
        </body>
    </html>
    """, subtype='html')
    return msg

def sendMail(message):
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com:465') as smtp:
            smtp.ehlo()
            smtp.starttls()
            # smtp.ehlo()
            smtp.login('your.gmail@gmail.com', 'your_password')
            smtp.send_message(message)
    except Exception as error:
        print(error)

for index, row in filterWhereEmailsNotSend(df).iterrows():
    msg = createEmailMessage(row.email)
    sendMail(msg)
    updateCsvRow(df, index)

print(df)
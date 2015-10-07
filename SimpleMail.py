from email.mime.text import MIMEText
import smtplib
import os
import os.path

class Mail(object):
    '''This class is used for loading smtp settings config file and sending email
       @param: config = dic obj whith the following
       host = smtp server
       port = smtp port number
       msg_from = sender email address
       msg_to = comma seprated list recipients
       username = username for logging into server
       password = your password
       isGmail = Boolean 
       requiresPassword = Boolean


    '''
    
    def __init__(self, config, **kwargs):
        #Set smtp server up
        self.host = config['host']
        self.port = config['port']
        self.msg_to = config['smtp_to']
        self.msg_from = config['smtp_from']
        self.username = config['username']
        self.password = config['password']
        self.isGmail = config['isGmail'] == True
        self.requiresPasssword = config['requiresPassword'] == True


    def send(self, msg, subject):
        '''Sends an email'''
         # Add the gmail smtp server
        server = smtplib.SMTP(host=self.host, port=self.port)
        #if this is gmail call ttls method
        if (self.isGmail): server.starttls()
        # login
        
        try:
            #Check if auth needed
            if (self.requiresPasssword): server.login(self.username, self.password)
            message = MIMEText(msg)
            message["To"] = self.msg_to
            message["From"] = self.msg_from
            message["Subject"] = subject

            print("Sending...")
            server.sendmail(self.msg_from, self.msg_to, message.as_string())
            print("Email was sent")
            server.close()

        except Exception as e:
            print(e)
            server.close()
        


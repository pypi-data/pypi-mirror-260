from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import traceback
import os
import inspect

class ErrorEmailer:
    def __init__(self, sender_email, sender_password, smtp_server, smtp_port, receiver_email=None):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        if not receiver_email:
            self.receiver_email = sender_email

    def send_email(self, function, exception, traceback_str):
        if callable(function):
            file_path = function.__code__.co_filename
            message = f"An error occurred in function '{function.__name__}': {str(exception)}"
        else:
            file_path = function
            message = f"An error occurred in file '{os.path.basename(file_path)}': {str(exception)}"
       
        project_directory = os.path.basename(os.path.dirname(file_path))

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = f"{project_directory} - Error Notification!"
        
        
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        error_message = f'''
        <html>
            <body>
                <h2>{message}</h2>
                <p>Time: {time}<br>File: {file_path}<br><br>Traceback:</p>
                <div style="background-color:#f8d7da; color:#721c24; border:1px solid #f5c6cb; border-radius:.25rem; padding:.5rem;">
                    <pre>{traceback_str}</pre>
                </div>
                <footer style="margin-top: 50px;">This is an automated email sent by EmailErrorMix.</footer>
            </body>
        </html>
        '''

        msg.attach(MIMEText(error_message, 'html'))

        try:            
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as smtp:
                smtp.login(self.sender_email, self.sender_password)
                smtp.send_message(msg)
            print("Error notification email sent successfully!")
        except Exception as e:
            print("Failed to send error notification email:", e)

    def notify_on_error(self):
        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    traceback_str = traceback.format_exc()
                    self.send_email(func, e, traceback_str)
                    raise e
            return wrapper
        return decorator
    
    def context_notify_on_error(self):
        caller_file = inspect.stack()[1].filename
        return ErrorContextManager(self, caller_file)
        

class ErrorContextManager:
    def __init__(self, error_emailer, caller_file):
        self.error_emailer = error_emailer
        self.caller_file = caller_file

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, e):
        if exc_type is not None:
            traceback_str = traceback.format_exc()
            self.error_emailer.send_email(self.caller_file, exc_value, traceback_str)
            raise e
        return True
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

send_email_declaration = {
    "name": "send_email",
    "description": "Send an email with a specified subject and body, with optional attachments.",
    "parameters": {
        "type": "object",
        "properties": {
            "sender_email": {
                "type": "string",
                "description": "The email address of the sender",
            },
            "sender_password": {
                "type": "string",
                "description": "The password or app-specific password of the sender's email account",
            },
            "recipient_email": {
                "type": "string",
                "description": "The email address of the recipient",
            },
            "subject": {
                "type": "string",
                "description": "The subject of the email",
            },
            "body": {
                "type": "string",
                "description": "The main content of the email",
            },
            "attachments": {
                "type": "array",
                "description": "List of file paths for any files to attach to the email",
                "items": {
                    "type": "string",
                    "description": "Path to an attachment file",
                },
            },
        },
        "required": [
            "sender_email",
            "sender_password",
            "recipient_email",
            "subject",
            "body",
        ],
    },
}


def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        # Set up the SMTP server
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create the email
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Connect to the server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        return "Email sent successfully"

    except Exception as e:
        return f"Failed to send email: {e}"

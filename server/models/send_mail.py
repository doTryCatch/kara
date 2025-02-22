import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

send_email_declaration = {
    "name": "send_email",
    "description": "Send an email with a specified subject and body, with optional attachments. If a previous email exists for the same recipient, modify the last sent email based on new instructions before resending. Append new content unless explicitly stated otherwise. Always display the final email content for confirmation before sending.",
    "parameters": {
        "type": "object",
        "properties": {
            "recipient_email": {
                "type": "string",
                "description": "The email address of the recipient. If modifying a past email, use the same recipient email unless specified.",
            },
            "subject": {
                "type": "string",
                "description": "The subject of the email. If modifying an existing email, keep the subject unchanged unless the user specifies a new one.",
            },
            "body": {
                "type": "string",
                "description": "The main content of the email. If modifying a previous email, append or update the content accordingly.",
            },
            "previous_email_reference": {
                "type": "boolean",
                "description": "Set to true if this email is a modification of a previously sent email.",
            },
            "attachments": {
                "type": "array",
                "description": "List of file paths for any files to attach to the email. If modifying a past email, retain previous attachments unless specified.",
                "items": {
                    "type": "string",
                    "description": "Path to an attachment file",
                },
            },
        },
        "required": [
            "recipient_email",
            "subject",
            "body"
        ],
    },
}def send_email(recipient_email, subject, body):
    sender_email="rp207045@gmail.com"
    sender_password="tsnv kvxq bwvd xybg"
    
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

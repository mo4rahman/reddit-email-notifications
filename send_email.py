"""
Basic Usage
Sending html/plain text to send email that includes a subject and body.

Sending email from GMAIL account.
NOTE: Make sure 2-Step Verification is turned off, and go to manage google
account, 'security' from the left menu, and then turn 'less secure app access'
to on, so we can have access and send through our gmails.
"""
import smtplib  # Authentication.
import ssl  # Secure socket layer.
from email.message import EmailMessage


def authenticate_email():
    """Checks to see if the email and password are correct credentials."""

    while True:
        sender_email = input("Please enter your gmail address: ")
        password = input("Please enter your password: ")

        # When we connect to GMAIL, we need a secure connection.
        # Context manager for a secure connection that we can use when we're using
        # smtp library and connecting to the gmail server.
        # Don't have our own mail server.
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as server:
            try:
                server.login(sender_email, password)
                print("Authenticated!")
                return sender_email, password
            except smtplib.SMTPAuthenticationError:
                print(
                    f"Sorry, your password: ({password}) doesn't match this gmail account: ({sender_email}). Please try again."
                )


def get_email_info(sender_email, password, body=None):
    """Asks for credentials and information we want to put into our email."""

    # Main things we need to write an email.
    subject = input("Please enter your subject here: ")
    if body is None:
        body = input("Please enter your body message here: ")
    receiver_email = input(
        "Please enter the email address you want to send your message to: "
    )
    return {
        "subject": subject,
        "body": body,
        "sender_email": sender_email,
        "receiver_email": receiver_email,
        "password": password,
    }


def build_email(sender_email, receiver_email, subject, body, html=None):
    """Builds the email and attaches each part respectively. Need email info (parameters)"""
    message = EmailMessage()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    if html:
        # HTML text in body
        message.add_alternative(html, subtype="html")
    else:
        message.set_content(body)  # Plain text in body
    return message


def send_email(message, sender_email, receiver_email, password):
    """Actually sending out the email by connecting to the gmail server and creating a
    context manager for a secure connection."""

    context = ssl.create_default_context()

    print("Sending email")  # Print to console so we know our program is working

    # Connecting with secure socket layer(ssl).
    # Connecting to gmail server using a secure way (ssl).
    with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=context) as server:

        server.login(
            sender_email, password
        )  # We assume correct from our authentication function.
        while True:
            try:
                server.sendmail(
                    from_addr=sender_email,
                    to_addrs=receiver_email,
                    msg=message.as_string(),
                )
                print("Success!")
                return
            except smtplib.SMTPRecipientsRefused:
                print("Sorry, you are sending to an invalid email address.")
                receiver_email = input(
                    "Please enter a valid email address to send to: "
                )
            # .as_string() converts our message body object into strings
            except smtplib.SMTPSenderRefused:
                print(
                    "Sorry, you are either sending too often or gmail has suspected spam. Please wait and try again later."
                )
                return


def main():
    """Runs email functions in this module"""
    sender_email, password = authenticate_email()
    email_info = get_email_info(sender_email, password)  # Returns a dictionary
    subject = email_info["subject"]
    body = email_info["body"]
    receiver_email = email_info["receiver_email"]
    html = f"""
    <html>
        <body>
            <h1>{subject}</h1>
            <h2>Testing second header</h2>
            <p1>{body}</p1>
        </body>
    </html>
    """
    message = build_email(sender_email, receiver_email, subject, body, html=html)

    send_email(
        message,
        sender_email,
        receiver_email,
        password,
    )


if __name__ == "__main__":
    main()

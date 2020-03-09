import smtplib
from email.mime.text import MIMEText

DOMAIN = "beta.donut.caltech.edu"


def send_email(to, text, subject, use_prefix=True, group=None):
    """
    Sends an email to a user. Expects 'to' to be a comma separated string of
    emails, and for 'msg' and 'subject' to be strings. If group
    is not none, the email is sent to a newsgroup and the to emails are hidden.
    """
    msg = MIMEText(text)
    if use_prefix and '[ASCIT Donut]' not in subject:
        subject = '[ASCIT Donut] ' + subject

    msg['Subject'] = subject
    msg['From'] = 'auto@' + DOMAIN
    if group:
        msg['To'] = group.lower().replace(' ', '_')
    else:
        msg['To'] = to

    with smtplib.SMTP('localhost') as s:
        s.sendmail('auto@' + DOMAIN, to, msg.as_string())

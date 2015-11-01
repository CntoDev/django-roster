"""
Created on Feb 17, 2012

@author: riaan
"""
# Import smtplib for the actual sending function
import smtplib
import os

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import logging

LOG = logging.getLogger(__file__)
LOG.setLevel(logging.INFO)


class Emailer(object):
    """Encapsulation for easy email sending

    """
    def __init__(self, host='localhost',
                 login_username=None,
                 login_password=None,
                 tls_port=None):
        self.host = host
        self.login_username = login_username
        self.login_password = login_password
        self.tls_port = tls_port

    def process_credentials(self, smtp_object):
        """

        :param smtp_object:
        :return:
        """
        if self.tls_port is not None:
            smtp_object.starttls()

        if self.login_username is not None:
            password = ""
            if self.login_password is not None:
                password = self.login_password

            smtp_object.login(self.login_username, password)

    def send_message(self, destination_email_address, source_email_address, subject, raw_msg, msg_type='plain'):
        """

        :param destination_email_address:
        :param source_email_address:
        :param subject:
        :param raw_msg:
        :param msg_type:
        :return:
        """
        destination_email_addresses = destination_email_address.split(";")
        # Create a text/plain message
        msg = MIMEText(raw_msg, msg_type)
        msg['Subject'] = subject
        msg['From'] = source_email_address
        msg['To'] = destination_email_address

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        smtp_instance = smtplib.SMTP(self.host)
        self.process_credentials(smtp_instance)
        smtp_instance.sendmail(source_email_address, destination_email_addresses, msg.as_string())
        smtp_instance.quit()

    def send_message_with_attachments(self, destination_email_address, source_email_address, subject, raw_msg,
                                      filename_pairs, msg_type='plain'):
        """

        :param destination_email_address:
        :param source_email_address:
        :param subject:
        :param raw_msg:
        :param filename_pairs:
        :param msg_type:
        :return:
        """
        msg = MIMEMultipart()

        destination_email_addresses = destination_email_address.split(";")

        msg['Subject'] = subject
        msg['From'] = source_email_address
        msg['To'] = destination_email_address

        # This is the textual part:
        part = MIMEText(raw_msg, msg_type)
        msg.attach(part)

        # This is the binary parts
        for filename_pair in filename_pairs:
            source_filename = filename_pair[0]
            email_filename = filename_pair[1]

            if os.path.isfile(source_filename):
                part = MIMEApplication(open(source_filename, "rb").read())
                part.add_header('Content-Disposition', 'attachment', filename=email_filename)
                msg.attach(part)
            else:
                LOG.warning(source_filename + " does not exist!")

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        smtp_istance = smtplib.SMTP(self.host)
        self.process_credentials(smtp_istance)

        smtp_istance.sendmail(source_email_address, destination_email_addresses, msg.as_string())

        smtp_istance.quit()

"""
This project allows sending STMP email over TLS using SSL.
Use the Emailer class to create an instance for an outgoing email account,
and call the send method to send an email. You can also use the EmailHandler
class to add a custom email handler to your app's logger.
"""

__version__ = "1.0.3"

from .sendmail import *

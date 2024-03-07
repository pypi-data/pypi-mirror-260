from __future__ import annotations

import os
import platform
import re
import subprocess
from datetime import datetime
from logging.handlers import SMTPHandler

try:
    import keyring
except ImportError:
    pass

machine = platform.node().lower()


class Emailer:
    def __init__(
        self,
        secure_host: str,
        port: int,
        email_address: str,
        password=None,
        user=None,
        unsecure_host: str = "",
        use_keyring: bool = False,
        include_ssl_status: bool = False,
    ) -> None:
        self.secure_host: str = secure_host
        self.include_ssl_status: bool = include_ssl_status
        self.bu_host: str = unsecure_host
        self.port: int = port
        self.email_address: str = email_address
        self.user: str = user or email_address
        self.user = self.email_address
        self.password: str = password or ""
        if use_keyring:
            self.password = keyring.get_password(self.email_address, self.user) or ""
            pass

    def __createMailMessage(
        self,
        subject: str,
        attachments: list[str],
        cc_list: list[str],
        bcc_list: list[str],
        html: bool,
        secure: bool = True,
    ) -> str:
        mail_msg: str = f"Send-MailMessage -From '{self.email_address}' -To $recipients"
        for cc in cc_list:
            mail_msg += f" -Cc '{cc}'"
        for bcc in bcc_list:
            mail_msg += f" -Bcc '{bcc}'"
        if len(attachments) > 0:
            mail_msg += (
                f""" -Attachments {", ".join([f"'{f}'" for f in attachments])}"""
            )
        mail_msg += f" -Subject '{subject}'"
        mail_msg += " -Body $EmailBody"
        if html:
            mail_msg += " -BodyAsHtml"
        mail_msg += f" -Port {self.port}"
        if secure:
            mail_msg += " -UseSSL"
            mail_msg += f" -Credential $mycreds"
        mail_msg += f" -smtpserver '{self.secure_host if secure else self.bu_host}'"
        return mail_msg

    def __send(
        self,
        to,
        subject: str,
        body: str,
        attachments: list[str] = [],
        cc_list: list[str] = [],
        bcc_list: list[str] = [],
        html: bool = False,
        secure: bool = True,
    ) -> subprocess.CompletedProcess:
        """
        Sends STMP email over TLS using SSL

        params
        ------
        to (str|list[str]): email recipient(s)
        subject (str): email subject line
        body (str): body of email as text or HTML string
        cc_list (list[str]): recipients to CC (default: [])
        bcc_list (list[str]): recipients to BCC (default: [])
        html (bool): whether to send body as HTML (default: False)
        secure (bool): whether to send with SSL (default: True)

        returns
        -------
        response (subprocess.CompletedProcess): exit code returned by cmd.exe after executing
            email send command
        """

        now: str = re.sub(r"[^0-9]", "", datetime.now().isoformat())
        status_str: str = "SSL" if secure else "non-SSL backup host"
        newline: str = "\n"
        if self.include_ssl_status:
            if html:
                body += f"<p>Email sent over {status_str}</p>"
            else:
                body += f"{newline}{newline}*** Email sent over {status_str} ***"
        tempfile: str = f"email_body_{now}.txt"
        with open(tempfile, "w") as f:
            f.write(body)

        to = to if isinstance(to, list) else [to]

        commands = []
        if secure:
            commands = [
                "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12",
                "$CurrentSecurityProtocol = [Net.ServicePointManager]::SecurityProtocol",
            ]

        commands = [
            *commands,
            f"""$recipients = {", ".join([f"'{addr}'" for addr in to])}""",
            f"$username = '{self.user}'",
            f"$password = '{self.password}'",
            f"$EmailBody = GET-Content -Raw -Path .\\{tempfile}",
        ]
        if secure:
            commands = [
                *commands,
                "$secpasswd = ConvertTo-SecureString $password -AsPlainText -Force",
                "$mycreds = New-Object System.Management.Automation.PSCredential ($username, $secpasswd)",
            ]
        commands.append(
            self.__createMailMessage(
                subject, attachments, cc_list, bcc_list, html, secure=secure
            ),
        )
        command = f'powershell -Command "{" ; ".join(commands)}'
        command += " ; "
        response = subprocess.run(f"cmd /c {command}", shell=False, capture_output=True)
        os.remove(tempfile)
        return response

    def send(
        self,
        to,
        subject: str,
        body: str,
        attachments: list[str] = [],
        cc_list: list[str] = [],
        bcc_list: list[str] = [],
        html: bool = False,
    ) -> subprocess.CompletedProcess:
        """
        Sends STMP email over TLS using SSL

        params
        ------
        to (str|list[str]): email recipient(s)
        subject (str): email subject line
        body (str): body of email as text or HTML string
        cc_list (list[str]): recipients to CC (default: [])
        bcc_list (list[str]): recipients to BCC (default: [])
        html (bool): whether to send body as HTML (default: False)

        returns
        -------
        response (subprocess.CompletedProcess): exit code returned by cmd.exe after executing
            email send command
        """
        args = [to, subject, body]
        kwargs = {
            "attachments": attachments,
            "cc_list": cc_list,
            "bcc_list": bcc_list,
            "html": html,
        }
        response = self.__send(*args, **kwargs)
        stderr = response.stderr.decode()
        if stderr != "":
            response = self.__send(*args, **kwargs, secure=False)
        return response


class EmailHandler(SMTPHandler):
    def __init__(
        self,
        mailhost,
        fromaddr: str,
        toaddrs,
        subject: str,
        credentials=None,
        secure=None,
        timeout: float = 5,
        send_html: bool = False,
        backup_host: str = "",
        include_ssl_status: bool = False,
    ) -> None:
        super().__init__(
            mailhost, fromaddr, toaddrs, subject, credentials, secure, timeout
        )
        self.send_html = send_html
        self.emailer = Emailer(
            (
                self.mailhost.split(":")[0]
                if isinstance(self.mailhost, str)
                else self.mailhost[0]
            ),
            self.mailport or 0,
            self.fromaddr,
            password=credentials[1] if credentials else None,
            use_keyring=False if credentials else True,
            unsecure_host=backup_host,
            include_ssl_status=include_ssl_status,
        )

    def emit(self, record) -> None:
        """
        Emit a record.

        Format the record and send it to the specified addressees.
        """
        try:
            result = self.emailer.send(
                self.toaddrs,
                self.getSubject(record),
                self.format(record),
                html=self.send_html,
            )
            stderr = result.stderr.decode()
            success = stderr == ""
            if not success:
                print(stderr)
        except Exception:
            self.handleError(record)

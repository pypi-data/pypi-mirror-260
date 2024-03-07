from __future__ import annotations

import json
import sys
from pathlib import Path
from random import choice
from string import ascii_letters

src_path = str(Path(__file__).absolute().parent.parent)
sys.path.append(src_path)

from src.secure_email import Emailer

with open("config.json", "r") as f:
    config = json.load(f)

emailer = Emailer(
    # Either supply a password or set use_keyring to True to use password saved in keyring
    # See readme for instructions on storing password in keyring
    config.get("host", ""),
    config.get("port", 0),
    config.get("from", ""),
    use_keyring=True,
    unsecure_host=config.get("bu_host", ""),
    include_ssl_status=True,
)

directory = Path(__file__).absolute().parent.joinpath("attachments")

txt = str(directory.joinpath("text_document.txt"))
img = str(directory.joinpath("image.png"))

menu = [
    "-" * 50,
    "Test email type (or <Enter> to exit):",
    "-" * 50,
    "",
    "1. Plain text email",
    "2. HTML email",
    "3. Email with attachment",
    "4. Email with multiple attachments",
    "5. Realy long email",
    "-" * 50,
    "Your response: ",
]


def randWord():
    limits = [i for i in range(3, 8)]
    return "".join([choice(ascii_letters) for _ in range(choice(limits))])


def randText(n):
    text = ""
    while len(text) < n:
        text = f"{text} {randWord()}".strip()
    return text[:n]


def printResult(result):
    stderr = result.stderr.decode()
    success = stderr == ""
    if not success:
        print(stderr)
    print(f"Email {'sent successfully' if success else 'failed'}")


while True:
    response = input("\n".join(menu))
    if response == "1":
        result = emailer.send(
            config.get("to", ""),
            "Plain text email",
            "Here is some plain text",
        )
        printResult(result)
    elif response == "2":
        result = emailer.send(
            config.get("to", ""),
            "HTML email",
            """
            <table role="presentation" border="0" align="center" cellpadding="12" width="600">
                <tr style="background-color: #008835; color: #fff; border: none;">
                    <h2 style="text-align: center; border: none;">Green header</h2>
                </tr>
            </table>
            <table
                role="presentation"
                border="1"
                cellpadding="6"
                align="center"
                width="600"
                border="0"
                style="border-collapse: collapse; background-color: #bddef1; color: #000;"
            >
                <tbody>
                    <tr><th>Row 1</th><td>Value 1</td></tr>
                    <tr><th>Row 2</th><td>Value 2</td></tr>
                    <tr><th>Row 3</th><td>Value 3</td></tr>
                </tbody>
            </table>
            """,
            html=True,
        )
        printResult(result)
    elif response == "3":
        result = emailer.send(
            config.get("to", ""),
            "Email with attachment",
            "Here is the gibberish you requested.",
            attachments=[txt],
        )
        printResult(result)
    elif response == "4":
        result = emailer.send(
            config.get("to", ""),
            "Email with multiple attachment",
            "Here are the random files you requested.",
            attachments=[txt, img],
        )
        printResult(result)
    elif response == "5":
        result = emailer.send(
            config.get("to", ""), "Really long email", randText(40_000)
        )
        printResult(result)
    if response == "":
        sys.exit()

import logging
import platform
import sys
import traceback
from functools import wraps
from pathlib import Path
from time import perf_counter
from typing import Any, Callable, Optional

from config import Config
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

src_path = str(Path(__file__).absolute().parent.parent.parent)
sys.path.append(src_path)

from src.secure_email import EmailHandler

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

from_: str = app.config.get("FROM", "")
to: str = app.config.get("TO", "")
host: str = app.config.get("HOST", "")
bu_host: str = app.config.get("BU_HOST", "")
user: str = f"lacsd.org\\{from_.split('@')[0]}"
port: int = app.config.get("PORT", 0)

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

default_formatter = logging.Formatter("%(levelname)s [%(asctime)s]: %(message)s")
email_formatter = logging.Formatter(
    "<p>%(levelname)s [%(asctime)s]:</p><p>%(message)s</p>"
)

fh = logging.FileHandler("logs.log")
fh.setLevel(logging.INFO)
fh.setFormatter(default_formatter)
mh = EmailHandler(
    (host, port),
    from_,
    to,
    "flask_mail_logger",
    send_html=True,
    backup_host=bu_host,
)
mh.setLevel(logging.ERROR)
mh.setFormatter(default_formatter)

logger.addHandler(fh)
logger.addHandler(mh)


def logRequest(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        result: Any
        try:
            start = perf_counter()
            result = func(*args, **kwargs)
            end = perf_counter()
            logger.info(f"{func.__name__} executed in {end - start:,.5f} seconds")
        except Exception as e:
            logger.error(
                f"{func.__name__} failed; {type(e).__name__}: {e} ({traceback.format_exc()})"
            )
            result = jsonify({type(e).__name__: str(e)})
        return result

    return wrapper


@app.route("/")
@logRequest
def home():
    return render_template("index.html")


@app.route("/api/set-number", methods=["POST"])
@logRequest
def setNumber():
    data: Optional[dict[str, Any]] = request.json
    if data:
        number: int = int(data.get("number", 0))
        # The line below ensures error if user enters 0 (or blank, since default is 0).
        # This is just to test the email handler, since the log level is set to ERROR
        _ = 2 / number
        return jsonify({"msg": f"Number {number} stored in database"})
    else:
        return jsonify({"msg": "No data received; nothing to update"})


if __name__ == "__main__":
    pc: str = platform.node()
    app.run(host=f"{pc}.lacsd.org", port=8888, debug=False)

#!/usr/bin/env python
import argparse

import aprslib
import logging

logger = logging.getLogger("aprst")

parser = argparse.ArgumentParser(
    prog="python -m aprst",
    description="APRS-IS feed polyfill creating status packet out of self to self message.",
)
parser.add_argument("callsign", type=str)
parser.add_argument("--host", type=str, default="rotate.aprs2.net")
parser.add_argument("--port", type=int, default=14580)
parser.add_argument("-v", "--verbose", action="count", default=0)
args = parser.parse_args()

if args.verbose == 1:
    logging.basicConfig(level=logging.INFO)
elif args.verbose >= 2:
    logging.basicConfig(level=logging.DEBUG)

CALLSIGN = args.callsign
HOST = args.host
PORT = args.port

status = ""


def fetch_status():
    logger.info("Fetching status...")

    def handler(data):
        if (
            data["format"] == "message"
            and data["addresse"] == CALLSIGN
            and data["from"] == CALLSIGN
        ):
            global status
            status = data["message_text"]
            raise StopIteration

    connection = aprslib.IS(CALLSIGN, "-1", HOST, PORT)
    connection.set_filter(f"b/{CALLSIGN} -t/poiqstunw")
    connection.connect()
    connection.consumer(handler)
    connection.close()
    logger.info("Status fetched!")


def send_status():
    logger.info("Sending status...")
    connection = aprslib.IS(CALLSIGN, aprslib.passcode(CALLSIGN), HOST, PORT)
    connection.set_filter(f"b/{CALLSIGN} -t/poimqstunw")
    connection.connect()
    connection.sendall(f"{CALLSIGN}>APRS,TCPIP*:>{status}")
    connection.close()
    logger.info("Status sent!")


while True:
    try:
        fetch_status()
        logger.info(f"{CALLSIGN} status is: {status}")
        send_status()
    except KeyboardInterrupt:
        break
    except Exception:
        logger.exception("Something went wrong, retrying...")

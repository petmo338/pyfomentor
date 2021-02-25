import logging
import argparse
import datetime
import sys
import os
import time
import json
# import configparser
from pyfomentor import connector

logger = logging.getLogger("Infomentor Notifier")

# config = configparser.ConfigParser()

# try:
#     config.read_file(open('informentor.ini'))
# except Exception as e:
#     logger.error('Config file error: {}'.format(e))


logformat = (
    "{asctime} - {name:25s}[{filename:20s}:{lineno:3d}] - {levelname:8s} - {message}"
)


def logtofile():
    from logging.handlers import RotatingFileHandler

    handler = RotatingFileHandler("log.txt", maxBytes=1024 * 1024, backupCount=10)
    logging.basicConfig(
        level=logging.INFO, format=logformat, handlers=[handler], style="{"
    )


def logtoconsole():
    logging.basicConfig(level=logging.DEBUG, format=logformat, style="{")


def parse_args(arglist):
    parser = argparse.ArgumentParser(description="Infomentor Grabber")
    parser.add_argument(
        "--nolog", action="store_true", help="print log instead of logging to file"
    )
    parser.add_argument("--username", type=str, nargs="?", help="infomentor username")
    parser.add_argument("--password", type=str, nargs="?", help="infomentor password")
    args = parser.parse_args(arglist)
    return args

def update(**kwargs):
    if 'username' in kwargs:
        user = kwargs['username']
        if not user:
            logger.critical('No username on command line')
            exit(3)
    
    if 'password' in kwargs:
        password = kwargs['password']
        if not password:
            logger.critical('No password on command line')
            exit(3)

    logger.info("==== USER: %s =====", user)
    now = datetime.datetime.now()
    im = connector.Infomentor(user)
    im.login(password)
    logger.info("User loggedin")
    statusinfo = {"datetime": now, "ok": False, "info": "", "degraded_count": 0}

    for pupil in im.get_pupils():
        im.change_pupil(pupil.get('id'))
        try:
            homework = im.get_homework()
            timetable = im.get_timetable()
            print(json.dumps({'pupil': pupil, 'homework': homework, 'timetable': timetable}))
            statusinfo["ok"] = True
            statusinfo["degraded"] = False
        except Exception as e:
            inforstr = "Exception occured:\n{}:{}\n".format(type(e).__name__, e)
            statusinfo["ok"] = False
            statusinfo["info"] = inforstr
            logger.exception("Something went wrong: {}".format(e))

def main():
    global logger
    args = parse_args(sys.argv[1:])
    if args.nolog:
        logtoconsole()
    else:
        logtofile()
    logger = logging.getLogger("Infomentor Notifier")
    logger.info("STARTING-------------------- %s", os.getpid())
    try:
        update(username=args.username, password=args.password)
    except Exception as e:
        logger.info("Exceptional exit")
        logger.exception("Info")
    finally:
        logger.info("EXITING--------------------- %s", os.getpid())


if __name__ == "__main__":
    main()

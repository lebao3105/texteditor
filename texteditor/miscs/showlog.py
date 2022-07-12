from os import getenv
import sys
import logging


if sys.platform == "win32":
    logfile = getenv("USERPROFILE") + "\.texted_log.log"
else:
    logfile = getenv("HOME") + "/.texted_log.log"

logging.basicConfig(level=logging.DEBUG, filename=logfile, 
        filemode="w", format='%(asctime)s : [%(levelname)s] - %(message)s')

logging.info('Started new logging session.')

def printdebug(message):
    logging.debug(message)

def throwerror(Exception):
    logging.error("Exception occured", exc_info=True)
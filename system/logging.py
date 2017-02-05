# coding=utf-8
import os
import time
import sys

from colorama import Fore, Style


class Logger(object):

    def __init__(self):

        # Check if the logs directory exists and make it if it doesnt
        if not os.path.exists("logs"):
            os.mkdir("logs")

    def _getTimestamp(self):
        """Get a timestamp in the correct format"""
        return time.strftime("[%d/%m/%Y] %H:%M:%S")

    def _write(self, file, message):
        """Write a message to a file"""
        fh = open("logs/" + file, "a")
        fh.write(message + "\n")
        fh.flush()
        fh.close()

    def _print(self, message):
        """Output to stdout"""
        sys.stdout.write(message + "\n")

    def _err(self, message):
        """Output to stderr"""
        sys.stderr.write(message + "\n")

    # Logging levels

    def debug(self, message, toFile=True):
        """Log message with DEBUG warning level"""
        f_string = self._getTimestamp() + " | DEBUG | %s" % message
        if toFile:
            self._write("debug.log", f_string)
        self._print(self._getTimestamp() + " | " + Fore.CYAN + "DEBUG" + Style.RESET_ALL + " | %s" % message)

    def info(self, message, toFile=True):
        """Log message with INFO warning level"""
        f_string = self._getTimestamp() + " | INFO | %s" % message
        if toFile:
            self._write("info.log", f_string)
        self._print(self._getTimestamp() + " | " + Fore.GREEN + "INFO" + Style.RESET_ALL + " | %s" % message)

    def warn(self, message, toFile=True):
        """Log message with WARN warning level"""
        f_string = self._getTimestamp() + " | WARN | %s" % message
        if toFile:
            self._write("warn.log", f_string)
        self._print(self._getTimestamp() + " | " + Fore.YELLOW + "WARN" + Style.RESET_ALL + " | %s" % message)

    def error(self, message, toFile=True):
        """Log message with ERROR warning level"""
        f_string = self._getTimestamp() + " | ERROR | %s" % message
        if toFile:
            self._write("error.log", f_string)
        self._err(self._getTimestamp() + " | " + Fore.RED + "ERROR" + Style.RESET_ALL + " | %s" % message)

#Logger()
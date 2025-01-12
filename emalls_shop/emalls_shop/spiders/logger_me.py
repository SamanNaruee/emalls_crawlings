import os
import sys
import scrapy
import logging
from scrapy.utils.log import configure_logging
from colorama import init, Fore, Style


def custom_log(message='', value=None, color=Fore.GREEN):
    """
    Print out colored messages in terminal with value and message.
    Args:
        value: The value to log
        message: Optional message (default: '')
        color: Color for the output (default: GREEN)
    Output:
        Logs file path, message, value(s), and function name in color
        Shows the target line in code that lead to error.
    """

    caller_frame = sys._getframe().f_back
    print(f"{color}\n##############################\n{Style.RESET_ALL}")
    print(f"{color}{message}{Style.RESET_ALL}")
    print(f"{color}Your value:\n{value}{Style.RESET_ALL}")
    print(f"{color}File path: {os.path.abspath(caller_frame.f_code.co_filename)}{Style.RESET_ALL}")
    print(f"{color}Function name: {caller_frame.f_code.co_name}{Style.RESET_ALL}")
    print(f"{color}Line number: {caller_frame.f_lineno}{Style.RESET_ALL}")
    with open(caller_frame.f_code.co_filename, 'r') as file:
        lines = file.readlines()
        target_line = lines[caller_frame.f_lineno - 1].strip()
    print(f"{color}Target line: {target_line}{Style.RESET_ALL}")
    print(f"{color}\n##############################\n{Style.RESET_ALL}")

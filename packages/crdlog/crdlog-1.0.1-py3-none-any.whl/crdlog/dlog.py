#! /usr/bin/env python
# -*- coding: utf-8 -*-
# * @author: dinglurong
# * @email: dinglurong@hotmail.com
# * @github: https://github.com/dingding-cc
# * @date: 2024/3/6 10:28
# * python version: python 3.10.10
""" =============================================================
                    Custom Logging
    1. Completed basic logging functionality,
    2. Completed colorful logging display.
================================================================"""

# * python base pkgs
import logging
# from logging import handlers
import os

# * python third party pkgs
import datetime as dt
import colorlog


class Log:
    """Initialize the logging

    Attributes:
    -----------
    * ``gen_log``: Whether to generate log files, default is False.
    * ``log_path``: the path to put log file
    * ``level``: the level of log
    * ``datefmt``: Timestamp format
    * ``fmt``: The format of message
    """
    
    # log level config
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    # colors config
    log_colors_config = {
        'DEBUG': 'white',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red'
    }

    def __init__(
        self,
        gen_log: bool = False,
        log_path: str = './',
        level: str = 'debug',
        datefmt: str = '%Y-%m-%d  %H:%M:%S',
        fmt: str = "[%(asctime)s.%(msecs)03d] "
            "line:%(lineno)d [%(levelname)s] : %(message)s"):
        # generate the log file meanwhile if the log file path is set
        if gen_log:
            self.logger = logging.getLogger()
            self.logger.setLevel(self.level_relations.get(level))

            # set the format for log file and console
            # format_file = logging.Formatter(fmt, datefmt=datefmt)
            format_console = colorlog.ColoredFormatter(
                fmt='%(log_color)s' + fmt,
                datefmt=datefmt,
                log_colors=self.log_colors_config)
            format_file = logging.Formatter(fmt, datefmt=datefmt)

            if not self.logger.handlers:
                #! call the stream handler for printing the message in console and input format
                sh = logging.StreamHandler()

                #! call the file handler for writing the message into log file
                now = dt.datetime.now()
                self.filename_path = now.strftime(
                    os.path.join(log_path, '%Y%m%d%H%M.log'))
                th = logging.FileHandler(
                    filename=self.filename_path,
                    encoding='utf-8')

                # format the message
                sh.setFormatter(format_console)
                th.setFormatter(format_file)

                # put the handler into the logger
                self.logger.addHandler(sh)
                self.logger.addHandler(th)

        else:
            self.logger = logging.getLogger()
            self.logger.setLevel(self.level_relations.get(level))
            # set the format for console
            format_console = colorlog.ColoredFormatter(
                fmt='%(log_color)s' + fmt,
                datefmt=datefmt,
                log_colors=self.log_colors_config)
            if not self.logger.handlers:
                # call the handler for printing the message in console and input format
                sh = logging.StreamHandler()
                sh.setFormatter(format_console)

                # put the handler into the logger
                self.logger.addHandler(sh)

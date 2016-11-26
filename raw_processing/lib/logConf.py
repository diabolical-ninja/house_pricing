"""
Title: logConf
Desc:  Configures logging settings
Author: Yassin Eltahir
Date: 2016-11-26
"""

import logging
import os.path
 

def initialize_logger(output_dir=None, log_name=None, console=True):
    """
    output_dir (path): Where should the log file be saved?
    log_name (str): What do you want the log file named?
    console (bool): Whether or not to print logging to console
    """
    
    # Set default output_dir
    if output_dir is None:
        output_dir='./'

    # If no log_name provided default to 
    if log_name is None:
        log_name='error'
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Capture all logging statements & output to file
    handler = logging.FileHandler(os.path.join(output_dir, "{}.log".format(log_name)),"w", encoding=None, delay="true")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if console is True:
        # Log Handler to display logging in Console
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
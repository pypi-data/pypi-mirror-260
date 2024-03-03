# jgtml
__version__ = "0.0.33"
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from jtc import (
    calculate_target_variable_min_max as calc_target_from_df,
    pto_target_calculation as calc_target_to_file,
    readMXFile as read
)

# from jgtpy import JGTPDS as pds,JGTADS as ads,JGTPDSP as pds

def __init__():
    """
    Initialize the jgtml module.
    """
    pass

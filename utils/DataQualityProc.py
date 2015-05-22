##################################################
# Data quality functions
# 
# Author: Ed Leming
# Date:   20/01/2014
##################################################


def check_trig_type(trigger_mask, criteria_mask = 32769, bit = 15):
    query_mask = 1 << bit
    if ((trigger_mask & query_mask) == (criteria_mask & query_mask) ) and ((criteria_mask & query_mask) == query_mask):
            return True
    return False

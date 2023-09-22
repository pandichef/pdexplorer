# ADDS A COLUMNS WITH THE DATE T+3 OR T+1, INCLUDING ALL HOLIDAY ADJUSTMENTS
# def t_plus(delta):
#     """Return number of days from today e.g., T+3"""
#     import pandas_market_calendars as mcal
#     import numpy as np
#     from datetime import date

#     nyse = mcal.get_calendar("NYSE")
#     holidays = nyse.holidays().holidays

#     date64 = np.datetime64("today") + delta

#     if date64.astype(date).isoweekday() == 6:
#         date64 += 2
#     elif date64.astype(date).isoweekday() == 7:
#         date64 += 1

#     while date64 in holidays:
#         date64 += 1

#     return date64.astype(date)

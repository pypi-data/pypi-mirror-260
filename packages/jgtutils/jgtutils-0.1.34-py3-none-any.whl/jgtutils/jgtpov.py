from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import tlid
import re


def get_dt_format_pattern(end_datetime):
  # List of possible datetime formats with corresponding regex patterns
  formats = [
    ("%Y-%m-%d", r"\d{4}-\d{2}-\d{2}$"),
    ("%y-%m-%d", r"\d{2}-\d{2}-\d{2}$"),
    ("%Y-%m-%d %H:%M", r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}$"),
    ("%y-%m-%d %H:%M", r"\d{2}-\d{2}-\d{2} \d{2}:\d{2}$"),
  ]
  dt_pattern = "%y-%m-%d"  # default

  # Try to match the end_datetime string with each pattern
  for date_format, pattern in formats:
    if re.match(pattern, end_datetime):
      dt_pattern = date_format
      break
  else:
    raise ValueError(f"Invalid date format in end_datetime: {end_datetime}")

  return dt_pattern

def calculate_start_datetime(end_datetime, timeframe, periods):
  # Check if end_datetime is in tlid format
  #date_format = "%Y-%m-%d" if len(end_datetime.split('-')[0]) == 4 else "%y-%m-%d"
  date_format = get_dt_format_pattern(end_datetime)
  
  #print("date_format: ",date_format)
  # Parse end_datetime string into datetime object
  end_datetime = datetime.strptime(end_datetime, date_format)
  
  
  # If the year is less than 100, add 2000 to it to get the correct century
  if end_datetime.year < 100:
      end_datetime = end_datetime.replace(year=end_datetime.year + 2000)
  #print(end_datetime)
  
  # Check if timeframe is in hours
  if timeframe.startswith('H'):
    # Convert timeframe from hours to minutes
    timeframe_minutes = int(timeframe[1:]) * 60
  elif timeframe.startswith('D'):
    # Convert timeframe from days to minutes
    timeframe_minutes = int(timeframe[1:]) * 24 * 60
  elif timeframe.startswith('W'):
    # Convert timeframe from weeks to minutes
    timeframe_minutes = int(timeframe[1:]) * 7 * 24 * 60
  elif timeframe.startswith('M'):
    # Convert timeframe from months to minutes
    # Assume an average of 30 days per month
    timeframe_minutes = int(timeframe[1:]) * 30 * 24 * 60
  elif timeframe.startswith('m'):
    # Convert timeframe from minutes
    timeframe_minutes = int(timeframe[1:])
  else:
    # Assume timeframe is already in minutes
    timeframe_minutes = int(timeframe)
  
  # Convert timeframe from minutes to seconds
  timeframe_seconds = timeframe_minutes * 60
  # Calculate total seconds for all periods
  total_seconds = timeframe_seconds * periods
  # Calculate start datetime
  start_datetime = end_datetime - timedelta(seconds=total_seconds)
  
  return start_datetime
def calculate_tlid_range(end_datetime, timeframe, periods):
  
  # Calculate start datetime
  start_datetime = calculate_start_datetime(end_datetime, timeframe, periods)
  
  dt_pattern = get_dt_format_pattern(end_datetime)
  start_datetime_formatted = start_datetime.strftime(dt_pattern)
  
  # Format start and end datetime to tlid format
  start_tlid = tlid.fromdtstr(start_datetime_formatted)
  end_tlid = tlid.fromdtstr(end_datetime)
  #print("LEnght of enddate:" , len(end_datetime))
  #print("dt_pattern: ",dt_pattern)
  
  # Return tlid range
  return f"{start_tlid}_{end_tlid}"




def calculate_quote_counts_tf(month_amount):
    # The base data
    M1 = month_amount
    W1 = M1 * 4 
    D1 = 22 * M1
    H8 = D1 * 3 
    H6 = D1 * 4 
    H4 = D1 * 6 
    H3 = D1 * 8 
    H2 = D1 * 12
    H1 = D1 * 24
    m30 = H1 * 2 
    m15 = H1 * 4 
    m5 = H1 * 12 
    m1 = H1 * 60

    # Create a dictionary with the calculated data
    data = {
        "M1": M1,
        "W1": W1,
        "D1": D1,
        "H8": H8,
        "H6": H6,
        "H4": H4,
        "H3": H3,
        "H2": H2,
        "H1": H1,
        "m30": m30,
        "m15": m15,
        "m5": m5,
        "m1": m1
    }

    return data


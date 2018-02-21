from datetime import date 
from datetime import timedelta

def get_dates(num_days):
    today=date.today()
    yesterday=today - timedelta(days=1)
    date_x = today- timedelta(days = num_days)
    yesterday_x = yesterday.isoformat()
    date_x = date2.isoformat()
    
    return date_x,yesterday_x

from datetime import datetime
import pytz

def get_current_data_time():
    timezone = pytz.timezone('America/Sao_Paulo')
    current_date = datetime.now(timezone).strftime('%Y-%m-%d %H:%M')
    return current_date
import datetime

MAX_UNITS = 2


def format_period(seconds):
    delta = datetime.timedelta(seconds=seconds)
    
    microseconds = delta.microseconds % 1000
    milliseconds = delta.microseconds // 1000
    seconds = delta.seconds % 60
    minutes = delta.seconds // 60 % 60
    hours = delta.seconds // (60 * 60)
    
    days = delta.days % 365
    years = delta.days // 365
    
    units = [f"{microseconds} microsecond{_get_plural(microseconds)}"]
    
    if milliseconds > 0:
        units.append(f"{milliseconds} millisecond{_get_plural(milliseconds)}")
    if seconds > 0:
        units.append(f"{seconds} second{_get_plural(seconds)}")
    if minutes > 0:
        units.append(f"{minutes} minute{_get_plural(minutes)}")
    if hours > 0:
        units.append(f"{hours} hour{_get_plural(hours)}")
    if days > 0:
        units.append(f"{days} day{_get_plural(days)}")
    if years > 0:
        units.append(f"{years} year{_get_plural(years)}")
    
    units.reverse()
    
    if len(units) > MAX_UNITS:
        units = units[0:MAX_UNITS]
    
    return ", ".join(units)
    

def _get_plural(count):
    return 's' if count != 1 else ''

from datetime import datetime, timedelta
def convertTimestamp(input):
    if input[len(input)-1] == 'Z':
        newTime = datetime.fromisoformat(input[:-1])
        return newTime.strftime("%Y/%m/%d, %H:%M:%S")+" (UTC)"

def thirtyDayInterval(input):
    if input[len(input)-1] == 'Z':
        newTime = datetime.fromisoformat(input[:-1])
    else:
        newTime = datetime.fromisoformat(input)
    tenDaysEarlier = newTime - timedelta(days=30)
    return [newTime.strftime("%Y-%m-%d"),tenDaysEarlier.strftime("%Y-%m-%d")]

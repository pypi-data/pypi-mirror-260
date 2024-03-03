from datetime import datetime


def zulu_time_now_str():
    return datetime.utcnow().isoformat()[:-3] + "Z"


# // Get the current date and time
# const currentDate = new Date();

# // Convert to ISO 8601 string (in UTC)
# const isoTimestamp = currentDate.toISOString();

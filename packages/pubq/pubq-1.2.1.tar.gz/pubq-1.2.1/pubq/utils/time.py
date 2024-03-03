from datetime import datetime


def getRemainingSeconds(timestamp):
    # Convert the timestamp to seconds
    target_time = timestamp

    # Get the current time in seconds
    current_time = datetime.now().timestamp()

    # Calculate the difference in seconds
    difference = target_time - current_time

    # Convert the difference to seconds
    remaining_seconds = int(difference)

    return remaining_seconds

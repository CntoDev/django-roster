from datetime import datetime, timedelta

import pytz
from django.utils import timezone


def dates_overlap(first_start_dt, first_end_dt, second_start_dt, second_end_dt):
    """

    :param first_start_dt:
    :param first_end_dt:
    :param second_start_dt:
    :param second_end_dt:
    :return:
    """
    overlaps = first_start_dt <= second_start_dt <= first_end_dt or first_start_dt <= second_end_dt <= first_end_dt
    envelops = second_start_dt <= first_start_dt and second_end_dt >= first_end_dt

    return overlaps or envelops


def calculate_dt_from_strings(dt_string, time_string):
    """

    :param dt_string:
    :param time_string:
    :return:
    """
    pytz.timezone("Europe/Stockholm")

    dt = datetime.strptime(dt_string, "%Y-%m-%d")

    time_parts = time_string.split("h")
    hour = int(time_parts[0])
    minute = int(time_parts[1])

    if hour >= 24:
        final_dt = timezone.make_aware(datetime(dt.year, dt.month, dt.day, 0, 0, 0), timezone.get_default_timezone())
        final_dt += timedelta(days=1, hours=hour - 24, minutes=minute)
    else:
        final_dt = timezone.make_aware(datetime(dt.year, dt.month, dt.day, hour, minute, 00),
                                       timezone.get_default_timezone())

    return final_dt

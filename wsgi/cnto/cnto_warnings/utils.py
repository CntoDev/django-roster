from datetime import datetime
from django.utils import timezone
from cnto_warnings.models import LowAttendanceWarning


def add_and_update_low_attendace_for_previous_month():
    """

    :return:
    """
    current_dt = timezone.now()
    previous_year_number = current_dt.year
    previous_month_number = current_dt.month - 1

    if previous_month_number < 1:
        previous_month_number = 12
        previous_year_number -= 1

    previous_month_start_dt = datetime(previous_year_number, previous_month_number, 1, 0, 0)

    print "Adding and updating attendance warnings..."
    start_count = LowAttendanceWarning.objects.all().count()
    LowAttendanceWarning.add_and_update_warnings_for_month(previous_month_start_dt)
    end_count = LowAttendanceWarning.objects.all().count()

    if start_count < end_count:
        print "Added %s low attendance warnings!" % (end_count - start_count)
    elif end_count < start_count:
        print "Removed %s low attendance warnings!" % (start_count - end_count)
    else:
        print "No change to attendance warnings!"

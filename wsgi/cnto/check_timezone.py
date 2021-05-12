from django.utils.timezone import datetime
from django.utils import timezone

dt = datetime.now()
current_dt = timezone.make_aware(dt, timezone.get_default_timezone())

print current_dt

import traceback

import valve.source.a2s
from django.core.exceptions import MultipleObjectsReturned
import pytz
from django.utils import timezone
from django.utils.timezone import datetime, timedelta
from django.http.response import JsonResponse
from django.shortcuts import redirect
from cnto import RECRUIT_RANK
from cnto.templatetags.cnto_tags import has_permission
from utils.date_utils import calculate_dt_from_strings

try:
    from sens_do_not_commit import ARMA3_SERVER_MONITOR
except ImportError:
    ARMA3_SERVER_MONITOR = ("localhost", 2303)
from utils.attendance_scraper import get_all_event_attendances_between
from ..models import Event, Member, Rank, Attendance, EventType


def interpret_raw_username(raw_username):
    """

    :param raw_username:
    :return:
    """
    username_parts = raw_username.split(" ")

    # Filter tags
    username_parts = [username_part.strip() for username_part in username_parts if
                      len(username_part) > 0 and username_part[0] != "["]

    username = " ".join(username_parts)
    return username


def scrape(request, event_type_name, dt_string, start_time_string, end_time_string):
    """Return the daily process main overview page.
    """

    try:
        if not request.user.is_authenticated():
            return redirect("login")
        elif not has_permission(request.user, "cnto_edit_events"):
            return redirect("manage")

        event_type = EventType.objects.get(name__iexact=event_type_name)

        start_dt = calculate_dt_from_strings(dt_string, start_time_string)
        end_dt = calculate_dt_from_strings(dt_string, end_time_string)

        if end_dt < start_dt:
            end_dt += timedelta(hours=24)

        try:
            scrape_result, scrape_stats = get_all_event_attendances_between(start_dt.astimezone(pytz.utc),
                                                                            end_dt.astimezone(pytz.utc))
        except ValueError:
            traceback.print_exc()
            scrape_result = {}
            scrape_stats = {'average_attendance': 0, 'minutes': 0, "success": True}

        # scrape_result = {u'Spartak [CNTO - Gnt]': 1.0, u'Chypsa [CNTO - Gnt]': 1.0, u'Guilly': 0.42857142857142855,
        # u'Hellfire [CNTO - SPC]': 1.0, u'Cody [CNTO - Gnt]': 1.0,
        # u'Ozzie [CNTO - SPC]': 0.7142857142857143, u'Skywalker': 0.6397515527950312,
        # u'Obi [CNTO - JrNCO]': 0.7142857142857143, u'Zero': 1.0,
        # u'Chris [CNTO - SPC]': 0.14285714285714285, u'Hateborder [CNTO - Gnt]': 1.0,
        # u'Dusky [CNTO - Gnt]': 0.7142857142857143}
        # scrape_stats = {'average_attendance': 0.7795031055900622, 'minutes': 56.0}

        try:
            event = Event.objects.get(start_dt__year=start_dt.year, start_dt__month=start_dt.month,
                                      start_dt__day=start_dt.day)

            event.start_dt = start_dt
            event.end_dt = end_dt

            event.event_type = event_type
            event.duration_minutes = scrape_stats["minutes"]
            event.save()
        except Event.DoesNotExist:
            event = Event(start_dt=start_dt, end_dt=end_dt,
                          duration_minutes=scrape_stats["minutes"], event_type=event_type)
            event.save()

        if len(scrape_result) > 0:
            # Only do something when data was collected.

            previous_attendances = Attendance.objects.filter(event=event)
            previous_attendances.delete()
            for raw_username in scrape_result:
                if len(raw_username.strip()) == 0:
                    continue

                username = interpret_raw_username(raw_username)

                if len(username) == 0:
                    continue

                rank_str = RECRUIT_RANK
                attendance_value = scrape_result[raw_username]

                try:
                    rank = Rank.objects.get(name__iexact=rank_str)
                except Rank.DoesNotExist:
                    rank = Rank(name=rank_str)
                    rank.save()

                try:
                    member = Member.objects.get(name__iexact=username, discharged=False, deleted=False)
                except Member.DoesNotExist:
                    member = Member(name=username, rank=rank)
                    member.save()
                except MultipleObjectsReturned:
                    raise ValueError("Multiple users found with name %s!" % (username,))

                attendance_seconds = (attendance_value * event.duration_minutes) * 60
                try:
                    attendance = Attendance.objects.get(event=event, member=member)
                    attendance.attendance_seconds = attendance_seconds
                    attendance.save()
                except Attendance.DoesNotExist:
                    attendance = Attendance(event=event, member=member,
                                            attendance_seconds=attendance_seconds)
                    attendance.save()
        return JsonResponse({"attendance": scrape_result, "stats": scrape_stats, "success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": traceback.format_exc()})


def update_attendance_for_current_event(update_interval_seconds=300, event_type_name="Unknown", event_start_hour=20):
    """None

    :return:
    """
    try:
        dt = datetime.now()

        start_dt = timezone.make_aware(datetime(dt.year, dt.month, dt.day, event_start_hour, 00, 00),
                                       timezone.get_default_timezone())

        current_dt = timezone.make_aware(dt, timezone.get_default_timezone())
        # pytz.timezone("Europe/Stockholm")
        #
        # if int(end_hour) >= 24:
        #     end_dt = timezone.make_aware(datetime(dt.year, dt.month, dt.day, 0, 0, 0),
        #                                  timezone.get_default_timezone())
        #     end_dt += timedelta(days=1, hours=int(end_hour) - 24)
        # else:
        #     end_dt = timezone.make_aware(datetime(dt.year, dt.month, dt.day, int(end_hour), 00, 00),
        #                                  timezone.get_default_timezone())
        #
        # if end_dt < start_dt:
        #     end_dt += timedelta(hours=240)
        #
        # event_duration_minutes = (end_dt - start_dt).total_seconds() / 60.0

        end_dt = current_dt + timedelta(seconds=update_interval_seconds)
        duration_minutes = (end_dt - start_dt).total_seconds() / 60.0

        try:
            event = Event.objects.get(start_dt__year=start_dt.year, start_dt__month=start_dt.month,
                                      start_dt__day=start_dt.day)
            end_dt = max(event.end_dt, end_dt)

        except Event.DoesNotExist:
            event_type = EventType.objects.get(name__iexact=event_type_name)

            event = Event(start_dt=start_dt, end_dt=end_dt, duration_minutes=duration_minutes, event_type=event_type)

        if event is None:
            raise ValueError("Could find appropriate event starting at %s", start_dt)

        event.start_dt = start_dt
        event.end_dt = end_dt

        event.duration_minutes = duration_minutes

        event.save()

        current_players = list_present_players_on_server()
        for raw_username in current_players:
            if len(raw_username.strip()) == 0:
                continue

            username = interpret_raw_username(raw_username)

            if len(username) == 0:
                continue

            rank_str = RECRUIT_RANK
            try:
                rank = Rank.objects.get(name__iexact=rank_str)
            except Rank.DoesNotExist:
                rank = Rank(name=rank_str)
                rank.save()

            try:
                member = Member.objects.get(name__iexact=username, discharged=False, deleted=False)
            except Member.DoesNotExist:
                member = Member(name=username, rank=rank)
                member.save()
            except MultipleObjectsReturned:
                raise ValueError("Multiple users found with name %s!" % (username,))

            try:
                attendance = Attendance.objects.get(event=event, member=member)
                attendance.attendance_seconds += update_interval_seconds
                attendance.save()
            except Attendance.DoesNotExist:
                attendance = Attendance(event=event, member=member,
                                        attendance_seconds=update_interval_seconds)
                attendance.save()
        return JsonResponse({"success": True, "error": None})
    except Exception as e:
        return JsonResponse({"success": False, "error": traceback.format_exc()})


def list_present_players_on_server():
    """

    :return:
    """
    server = valve.source.a2s.ServerQuerier(ARMA3_SERVER_MONITOR)
    response = server.get_players()
    players = [player["name"] for player in response["players"]]

    return players


if __name__ == "__main__":
    print("YES")

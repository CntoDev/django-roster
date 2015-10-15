import traceback
import logging
import urllib
import threading

from datetime import datetime
from bs4 import BeautifulSoup

LOG = logging.getLogger("roster-tracker")
LOG.setLevel(logging.DEBUG)

FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

CH = logging.StreamHandler()
CH.setLevel(logging.DEBUG)
CH.setFormatter(FORMATTER)
LOG.addHandler(CH)

MINIMUM_ATTENDANCE_NUMBER = 5


class ScrapeThread(threading.Thread):
    def __init__(self, viewer, start_dt, end_dt):
        threading.Thread.__init__(self)
        self._viewer = viewer
        self._start_dt = start_dt
        self._end_dt = end_dt

    def run(self):
        self._viewer.busy_signal.emit(True)
        try:
            scraped_result, scrape_stats = get_all_event_attendances_between(self._start_dt, self._end_dt)
            self._viewer.scraped_result_signal.emit(self._start_dt.date(), scraped_result)
            self._viewer.show_message_signal.emit("Success",
                                                  "Scraped succesfully for %s players with an average attendance of %s\n"
                                                  "minutes out of a total played time of %s minutes!" % (
                                                  len(scraped_result),
                                                  int(scrape_stats["minutes"] * scrape_stats["average_attendance"]),
                                                  int(scrape_stats["minutes"])))

        except Exception, e:
            self._viewer.show_message_signal.emit("Error", str(traceback.format_exc()))
        self._viewer.busy_signal.emit(False)


def get_url_for_event_page(page_number=1):
    """
    """
    return "http://arma3.swec.se/server/data/179899?page=%s" % (page_number,)


def complete_event_url(partial_event_url):
    """
    """
    return "http://arma3.swec.se" + partial_event_url


def get_all_events_for_page(page_number=1):
    """
    """
    event_url = get_url_for_event_page(page_number)
    LOG.info("Loading all events for page %s...", event_url)
    page_file = urllib.urlopen(event_url)
    # page_file = open("temp.html", "r") 
    soup = BeautifulSoup(page_file, "lxml")

    if soup is None:
        raise ValueError("No soup!")

    def full_table(tag):
        """
        """
        if tag.name.lower() != "table":
            return False

        if not tag.has_attr("class"):
            return False

        if "full" not in [class_name.lower() for class_name in tag["class"]]:
            return False

        for child in tag.parent.parent.children:
            if child.name == "h2":
                if child.text.lower() == "game history":
                    return True

        return False

    found_full_table = soup.find_all(full_table)[0]

    all_event_dicts = {}

    event_rows = found_full_table("tr")
    for event_row in event_rows:
        if len(event_row("th")) > 0:
            continue

        column_values = event_row("td")

        event_url = column_values[0]("a")[0]["href"]
        players_string = column_values[1].text
        start_dt_string = column_values[3].text
        start_dt = datetime.strptime(start_dt_string, "%Y-%m-%d %H:%M")
        end_dt_string = column_values[4].text
        try:
            end_dt = datetime.strptime(end_dt_string, "%Y-%m-%d %H:%M")
        except ValueError:
            end_dt = None

        all_event_dicts[start_dt] = {
            "player_count": int(players_string.split("/")[0]),
            "event_url": complete_event_url(event_url),
            "end_dt": end_dt
        }

    return all_event_dicts


def get_all_events_from_start_to_end(start_dt, end_dt):
    """
    """

    current_page = 1

    all_event_dicts = {}

    while len(all_event_dicts) == 0 or min(all_event_dicts) > start_dt:
        page_events = get_all_events_for_page(current_page)

        all_event_dicts.update(page_events)

        current_page += 1

    sorted_start_dts = sorted(all_event_dicts.keys())

    relevant_events = {}
    for event_start_dt in sorted_start_dts:
        event = all_event_dicts[event_start_dt]
        event_end_dt = event["end_dt"] if event["end_dt"] is not None else end_dt

        player_count = event["player_count"]

        if (
                    start_dt <= event_start_dt <= end_dt or start_dt <= event_end_dt <= end_dt) and player_count > MINIMUM_ATTENDANCE_NUMBER:
            event_start_dt = max(event_start_dt, start_dt)
            event["end_dt"] = min(event_end_dt, end_dt)
            relevant_events[event_start_dt] = event

    return relevant_events


def get_attendance_rates_from_event_url(event_url):
    """
    """
    LOG.info("Loading event attendance rates from %s...", event_url)
    page_file = urllib.urlopen(event_url)
    # page_file = open("event.html", "r") 
    soup = BeautifulSoup(page_file, "lxml")

    if soup is None:
        raise ValueError("No soup!")

    def full_table(tag):
        """
        """
        if tag.name.lower() != "table":
            return False

        if not tag.has_attr("class"):
            return False

        if "full" not in [class_name.lower() for class_name in tag["class"]]:
            return False

        for child in tag.parent.children:
            if child.name == "h2":
                if child.text.lower() == "players":
                    return True

        return False

    found_full_table = soup.find_all(full_table)[0]

    all_player_attendances = {}

    player_rows = found_full_table("tr")
    for player_row in player_rows:
        if len(player_row("th")) > 0:
            continue

        column_values = player_row("td")
        player_name = column_values[0].text
        attendance_style = column_values[3]("div")[0]["style"]
        attendance_parts = [part.strip() for part in attendance_style.split(";")]
        attendance_parts_dict = {}
        for part in attendance_parts:
            part_parts = part.split(":")
            attendance_parts_dict[part_parts[0].strip()] = int(part_parts[1].strip().replace("%", ""))

        attendance = attendance_parts_dict["width"] / (
        100.0 - attendance_parts_dict["margin-right"] - attendance_parts_dict["margin-left"])
        all_player_attendances[player_name] = attendance

    return all_player_attendances


def get_all_event_attendances_between(start_dt, end_dt):
    """
    """
    events = get_all_events_from_start_to_end(start_dt, end_dt)
    if len(events) == 0:
        raise ValueError("No events took place in specified time frame!")

    overall_attendances = {}
    total_events_minutes = 0
    for event_start_dt in sorted(events):
        event = events[event_start_dt]
        event_url = event["event_url"]
        event_end_dt = event["end_dt"]
        if event_end_dt is None:
            LOG.critical("Assuming end of search date is relevant as event is still ongoing.")
            event_end_dt = end_dt
        event_minutes = ((event_end_dt - event_start_dt).total_seconds()) / 60.0
        total_events_minutes += event_minutes

        LOG.info("Getting attendance rates from %s to %s...", event_start_dt, event_end_dt)

        event_attendances = get_attendance_rates_from_event_url(event_url)

        for player_name in event_attendances:
            if player_name not in overall_attendances:
                overall_attendances[player_name] = 0

            overall_attendances[player_name] += event_attendances[player_name] * event_minutes

    average_attendance = 0
    for player_name in overall_attendances:
        overall_attendances[player_name] /= total_events_minutes
        average_attendance += overall_attendances[player_name]

    average_attendance /= len(overall_attendances)

    return overall_attendances, {"minutes": total_events_minutes, "average_attendance": average_attendance}


# if __name__ == "__main__":
# LOG.info("CNTO roster tracker 0.1.0 by Supreme (sakkie99@gmail.com)")
#     print """
# Commands:
#  * import-event: Specify start and end datetime to integrate event from.
#    e.g. roster-tracker import-event 2015-10-10 18:00 20:00
#  """
#
#     parser = argparse.ArgumentParser(description="Process events from CNTO server monitor.")
#
#     parser.add_argument(dest='command',
#                         type=str,
#                         help='Command you wish to execute.')
#
#     parser.add_argument(dest='event_date',
#                         type=str,
#                         help='Command you wish to execute.')
#
#     args = parser.parse_args()
#
#     LOG.info("Starting roster retrieval...")
#
#     if args.command.lower() == "import-event":
#         if len(sys.argv) < 4:
#             raise ValueError("Too few arguments provided, check example for command!")
#         print sys.argv[2]

#     start_dt = datetime(2015, 10, 10, 18, 00, 00)
#     end_dt = datetime(2015, 10, 12, 20, 00, 00)
#     
#     # overall_attendances = get_all_event_attendances_between(start_dt, end_dt)
#     overall_attendances = {u'Spartak [CNTO - Gnt]': 1.0, u'Chypsa [CNTO - Gnt]': 0.27631578947368424, u'Anders [CNTO - SPC]': 0.7236842105263158, u'Guilly': 0.7236842105263158, u'Hellfire [CNTO - SPC]': 1.0, u'Rush [CNTO - Gnt]': 0.7236842105263158, u'Hateborder [CNTO - Gnt]': 0.7236842105263158, u'Peltier [CNTO - Gnt]': 0.5394736842105263, u'John [CNTO - JrNCO]': 0.7236842105263158, u'Alos': 1.0, u'Highway [CNTO - Gnt]': 0.27631578947368424, u'Mars [CNTO - Gnt]': 0.7236842105263158, u'Skywalker [CNTO - Gnt]': 0.6052631578947368, u'Supreme [CNTO - Gnt]': 0.7236842105263158, u'Dachi [CNTO - Gnt]': 0.7236842105263158, u'Postma [CNTO - Gnt]': 0.7236842105263158, u'Obi [CNTO - JrNCO]': 0.39473684210526316, u'Chris [CNTO - SPC]': 1.0, u'Cody [CNTO - SPC]': 1.0}
#     
#     db = RosterDatabase("temp.sqlite")
#     db.insert_attendances(start_dt.date(), overall_attendances)

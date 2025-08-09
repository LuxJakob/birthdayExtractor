import csv
from datetime import datetime
from uuid import uuid4

CONTACTS_FILE = "../contacts.csv"
OUTPUT_ICS_FILE = "birthdays.ics"

def parse_date(date_str):
    date_str = date_str.strip()
    if not date_str:
        return None
    # Format YYYY-MM-DD
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        pass
    # Format --MM-DD (Google partial date without year)
    try:
        return datetime.strptime(date_str, "--%m-%d")
    except ValueError:
        pass
    return None

def create_alarm(trigger, description):
    """Creates a VALARM block."""
    return "\n".join([
        "BEGIN:VALARM",
        "ACTION:DISPLAY",
        f"DESCRIPTION:{description}",
        f"TRIGGER:{trigger}",
        "END:VALARM"
    ])

def create_ics_event(name, date_obj):
    uid = str(uuid4())

    # Reminder triggers:
    # -21 days  → -P21D
    # -7 days   → -P7D
    # same day 09:00 → PT9H after midnight
    alarms = [
        create_alarm("-P21D", f"{name}'s birthday in 3 weeks"),
        create_alarm("-P7D", f"{name}'s birthday in 1 week"),
        create_alarm("PT9H", f"{name}'s birthday today")
    ]

    return "\n".join([
        "BEGIN:VEVENT",
        f"UID:{uid}",
        f"DTSTART;VALUE=DATE:{date_obj.strftime('%Y%m%d')}",
        "RRULE:FREQ=YEARLY",
        f"SUMMARY:Birthday: {name}",
        "TRANSP:TRANSPARENT",
        *alarms,
        "END:VEVENT"
    ])

def main():
    events = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Birthday Exporter//EN"]

    with open(CONTACTS_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            name_parts = [row.get("First Name", "").strip(),
                          row.get("Middle Name", "").strip(),
                          row.get("Last Name", "").strip()]
            name = " ".join(filter(None, name_parts)) or "Unknown"

            birthday_str = row.get("Birthday", "").strip()
            date_obj = parse_date(birthday_str)

            # Check Event columns if no direct Birthday
            if not date_obj:
                for i in range(1, 5):
                    if row.get(f"Event {i} - Label", "").lower() == "birthday":
                        date_obj = parse_date(row.get(f"Event {i} - Value", ""))
                        if date_obj:
                            break

            if date_obj:
                events.append(create_ics_event(name, date_obj))

    events.append("END:VCALENDAR")

    with open(OUTPUT_ICS_FILE, "w", encoding="utf-8") as icsfile:
        icsfile.write("\n".join(events))

    print(f"✅ Done! {OUTPUT_ICS_FILE} created with recurring birthdays and reminders.")

if __name__ == "__main__":
    main()

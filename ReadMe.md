# Get Birthdays from Google Contacts into Google Calendar

Extract birthdays from your exported Google Contacts CSV and add them to your calendar as **recurring yearly events** with reminders.

## Usage
1. **Export contacts** from [Google Contacts](https://contacts.google.com/)  
   - Click **More → Export → Google CSV**  
   - Save as `contacts.csv`

2. **Run script**  
   ```bash
   cd src
   python3 contacts_birthdays_to_ics.py

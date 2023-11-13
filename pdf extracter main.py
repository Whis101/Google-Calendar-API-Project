import tabula
import pandas as pd
from tabulate import tabulate
import datetime
from datetime import datetime
import re
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

def main():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_info("token.json")
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_taken:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json.json",SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json",'w') as token:
            token.write(creds.to_json())


    try:
        service = build("calendar","v3",credentials=creds)

        now =
    except HttpError as error:
        print("An error occured:", error)






# USED TO MATCH MONTH NAME TO A NUMBER THAT REPRESENTS ITS ORDER IN THE YEAR
month_dict = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}

# CONVERT PDF TO CSV THATS EASIER TO WORK WITH
tabula.convert_into("fall2023calendar.pdf","fall2023calendar.csv",output_format="csv",pages='all')
# READ CSV INTO A DATA-FRAME
df = pd.read_csv("fall2023calendar.csv")

# RENAME THE COLUMN BECAUSE IT IS UNNAMED
df = df.rename(columns={'Unnamed: 0':'Dates','Unnamed: 1':'Events'})

# INITIALIZE A LIST TO APPEND WITH STRINGS
date_strings = list()

# DEFINE FUNCTION TO EXTRACT DATE USING REGEX
def extract_date(date_string):

    # DEFINE REGEX PATTERN THAT LOOKS FOR THE PATTERN "DAY, MONTH DATE"
    match = re.match(r'(\w+), (\w+) (\d+)', date_string)
    # IF MATCH IS FOUND RETURN MONTH AND DATE
    if match:
        return match.group(2), match.group(3)
    else:
        return None, None

# DEFINE FUNCTION TO CONVERT THE MONTH AND DATE FROM EXTRACT_DATE FUNCTION TO CONVENTIONAL FORMAT
def convert_to_conventional_format(date_string):
    if "Semester" in date_string  or 'nan' in date_string:
        return None  # Return None for strings indicating a semester, as they don't represent specific dates

    try:
      # Check if the date string contains all necessary parts
        month_name, day = extract_date(date_string)
        month = month_dict[month_name]

            # Create a datetime object
        date_obj = datetime(year=datetime.now().year, month=month, day=int(day))

            # Format the datetime object as "Wednesday, October 18"
        formatted_date = date_obj.strftime(f"{datetime.now().year}, %B %d")
        return formatted_date
         
    except ValueError:
        return None


# Example usage


for date_string in df['Dates']:
    date_strings.append(str(date_string))

date_pattern = r"\b(?:\w+, )?(?:\w+ - )?\w+\s\d{1,2}(?: - \d{1,2})?\b"
proper_matches = list()
for date_string in date_strings:
    matches = re.findall(date_pattern, date_string)
    if matches:
        proper_matches.append(matches[0])
        print(matches[0])
formatted_dates = list()
for date_string in proper_matches:
    formatted_date = convert_to_conventional_format(date_string)
    if formatted_date is not None:
        formatted_dates.append(formatted_date)

print(formatted_dates)














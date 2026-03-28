"""
# ReDI School - F25 Python Foundations Online
# Events Analysis - December 2025
Inês Tomás & Botros Attia -
"ReDI Calendar"
"""

# Import needed libraries
import csv
import pandas as pd
import plotly.express as px

# Store name of dataset csv as a variable
dataset_csv = "Germany Tech Events 2020-2024.csv"

"""# My Calendar
This is a list of dictionaries that will the structure of our calendar.
"""

my_calendar = [
    {
        "name": "Studying Workshop",
        "date": "2025-10",
        "type": "meetup",
        "recurrence": "one-off",
        "city": "Berlin",
        "topic": "python",
        "participants": "15",
        "format": "online"
    },
    {
        "name": "ReDI Session",
        "date": "2025-10",
        "type": "conference",
        "recurrence": "recurring",
        "city": "Berlin",
        "topic": "python",
        "participants": "15",
        "format": "online"
    },
    {
        "name": "Project Work",
        "date": "2025-10",
        "type": "hackathon",
        "recurrence": "one-off",
        "city": "Berlin",
        "topic": "data science",
        "participants": "5",
        "format": "online"
    }
]

df_my_calendar = pd.DataFrame(my_calendar)
df_my_calendar

"""# Import Events
This function imports external data to the calendar
"""

# This is used to upload data from the drive to the notebook
from google.colab import files
document = files.upload()

# This is used to import all the data of the external file to our calendar
def load_csv(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

csv_events = load_csv(dataset_csv)
full_calendar = my_calendar + csv_events

df_full_calendar = pd.DataFrame(full_calendar)
df_full_calendar

"""# Feature Functions

This block of functions sets the features of the Calendar:


Add Event

Edit Event

Delete Event

View Event
"""

#ADD EVENT
def add_event(calendar, name, date, type, recurrence, city, topic, participants, format):
# Check if an event already exists at the same date and time
  for event in calendar:
    if event["name"] == name and event["date"] == date:
      print("There's already an event at this time!")
      return
# If no conflict, add the event
  calendar.append({
      "name": name,
      "date": date,
      "type": type,
      "recurrence": recurrence,
      "city": city,
      "topic": topic,
      "participants": participants,
      "format": format
        })
  print("New event added successfully!")


#EDIT EVENT
def edit_event(calendar, name_find, date_find, name=None, date=None, type=None, recurrence=None, city=None, topic=None, participants=None, format=None):
  for event in calendar:
    if event["name"] == name_find and event["date"] == date_find:
      # Update only fields that are provided
      if name:
        event["name"] = name
      if date:
        event["date"] = date
      if type:
        event["type"] = type
      if recurrence:
        event["recurrence"] = recurrence
      if city:
        event["city"] = city
      if topic:
        event["topic"] = topic
      if participants:
        event["participants"] = participants
      if format:
        event["format"] = format
      print("Event updated successfully!")
      return
# If no matching event was found
  print(f"No event found named '{name_find}' on this date '{date_find}'.")


#DELETE EVENT
def delete_event(calendar, name, date):
  for event in calendar:
    if event["name"] == name and event["date"] == date:
      calendar.remove(event)
      print("Event deleted successfully!")
      return
  # If no matching event was found
  print("No events found on this day.")


#VIEW EVENT
def view_event(calendar, name, date):
  for event in calendar:
    if event["name"] == name and event["date"] == date:
      display(pd.DataFrame([event]))
      return
  # If no matching event was found
  print("No events found on this day.")

"""# Helper Functions

This block of functions is designed to relief the main function workload, and divide tasks better:

Add Event Details

Edit Event Details

Delete Event Details

View Event Details

Clean Data
"""

#ADD EVENT DETAILS
def add_event_details():
  print(" Please enter the following Event Details: ")
  name = input(" Name: ")
  date = input(" Date (YYYY-MM): ")
  type = input(" Type: ")
  recurrence = input(" Recurrence: ")
  city = input(" City: ")
  topic = input(" Topic: ")
  participants = input(" Participants: ")
  format = input(" Format: ")

  return {
      "name": name,
      "date": date,
      "type": type,
      "recurrence": recurrence,
      "city": city,
      "topic": topic,
      "participants": participants,
      "format": format
  }


#EDIT EVENT DETAILS
def edit_event_details():
  print(" Find Event to Edit: ")
  name_find = input(" Enter the Name of the event you would like to modify: ")
  date_find = input(" Enter the Date (YYYY-MM) of the event to modify: ")
  print(" Enter the New Details (Press Enter to keep the original value): ")
  name = input(" New Name: ") or None
  date = input(" New Date: ") or None
  type = input(" New Type: ") or None
  recurrence = input(" New Recurrence: ") or None
  city = input(" New City: ") or None
  topic  = input(" New Topic: ") or None
  participants = input(" New Participants: ") or None
  format = input(" New Format: ") or None

  return (
      name_find,
      date_find,
      {
          "name": name,
          "date": date,
          "type": type,
          "recurrence": recurrence,
          "city": city,
          "topic": topic,
          "participants": participants,
          "format": format
      }
  )


#DELETE EVENT DETAILS
def delete_event_details():
  print(" Find Event to Delete: ")
  name = input(" Name: ")
  date = input(" Date: ")
  return name, date


#VIEW EVENT DETAILS
def view_event_details():
  print(" Find Event to View: ")
  name = input(" Name: ")
  date = input(" Date: ")
  return name, date


#CLEAN DATA
def clean_data(data_file):
  entrys_clean = ['name', 'type', 'recurrence', 'city', 'topic', 'format']
  for event in data_file:
    for key in entrys_clean:
      if key in event and isinstance(event.get(key), str):
        event[key] = event[key].strip().title()

  df_calendar = pd.DataFrame(data_file)
  df_calendar.columns = [col.title() for col in df_calendar.columns]

  df_calendar['Date'] = pd.to_datetime(df_calendar['Date'], format='%Y-%m', errors='coerce')
  df_calendar['Date'] = df_calendar['Date'].dt.strftime('%Y-%m')
  df_calendar['Participants'] = pd.to_numeric(df_calendar['Participants'], errors='coerce')

  return df_calendar

"""# Interactive my_application function
This is our Calendar App, and our main function. Here are all the previous functions combined and the user is able to use each of them individually.
There is the possibility to keep using the app or just exit it after every use.
"""

def my_application(calendar):
  app_running = True

  while app_running:
    what_to_do = input(" What do you want to do to your calendar? \n Add Event \n Edit Event \n Delete Event \n View Event \n").lower().strip()

    #Add Event
    if what_to_do == "add event":
      details = add_event_details()
      add_event(calendar, **details)

    #Edit Event
    elif what_to_do == "edit event":
      name_find, date_find, updates_dict = edit_event_details()
      edit_event(calendar, name_find, date_find, **updates_dict)

    #Delete Event
    elif what_to_do == "delete event":
      name, date = delete_event_details()
      delete_event(calendar, name, date)

    #View Event
    elif what_to_do == "view event":
      name, date = view_event_details()
      view_event(calendar, name, date)

    #Invalid Input
    else:
      print(" Invalid input. Please try again. ")

  #Keep running or Exit
    again = input(" Would you like to do anything else? Yes/No ").lower().strip()
    if again != "yes":
      app_running = False
      print("\nGoodbye :)\n")
      display(clean_data(full_calendar))
df_calendar = clean_data(full_calendar)

# Demo main function
my_application(full_calendar)

df_calendar = clean_data(full_calendar)

"""# Analyses of the Calendar Data"""

# Graph n1
# Pie chart about the density of events in each city

analysis_1 = px.pie(
    df_calendar, names="City",
    title='Tech Events Across Different Cities')
analysis_1.show()

# Graph n2
# Line chart about the density of events over time

monthly_counts = df_calendar.groupby('Date').size().reset_index(name='N of Events')
analysis_2 = px.line(
    monthly_counts,
    x='Date',
    y='N of Events',
    title='Tech Events Over Time (Monthly)'
)
analysis_2.show()

# Graph n3
# Bar chart about the density of types of events

type_counts = df_calendar.groupby('Type').size().reset_index(name='N of Types')
analysis_3 = px.bar(
    type_counts,
    x='Type',
    y='N of Types',
    title='Tech Events Different Types '
)
analysis_3.show()

# Graph n4
# Scatter plot about the number of Events for each topic

topic_counts = df_calendar.groupby('Topic').size().reset_index(name='N of Events')
analysis_4 = px.scatter(
    topic_counts,
    x='Topic',
    y='N of Events',
    title='Tech Events Different Types '
)
analysis_4.show()

# Graph 5
# Bar chart about the average of participants for each event format

format_avg = df_calendar.groupby('Format')['Participants'].mean().reset_index()

analysis_5 = px.bar(
    format_avg,
    x='Format',
    y='Participants',
    title='Average Participants by Event Format',
    labels={'participants':'Average Participants', 'format':'Event Format'}
)

analysis_5.show()

#Graph 6
#Heatmap that describes the density of avg n of events per tipy per city
df_copy = df_calendar.copy()

# Create pivot table
pivot = df_copy.pivot_table(
    index='City',
    columns='Topic',
    values='Participants',
    aggfunc='mean'
)
pivot = pivot.fillna(0)

# Plot heatmap
analysis_6 = px.imshow(
    pivot,
    labels=dict(
        x="Topic",
        y="City",
        color="Avg Participants"
    ),
    title="Heatmap: City vs Topic (Average Participants)",
    aspect="auto",
    color_continuous_scale="Blues"
)

analysis_6.update_xaxes(side="top")

analysis_6.show()

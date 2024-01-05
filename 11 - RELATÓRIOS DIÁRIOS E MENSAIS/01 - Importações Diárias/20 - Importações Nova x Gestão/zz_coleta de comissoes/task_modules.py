from datetime import datetime, timezone
import requests
from dotenv import dotenv_values

users_id={
  "Matheus":61030593,
  "Cleiton":61030565,
  "Claudinei":61030590,
  "Sheila":61030585
}

def get_users():
  params = dotenv_values(".env")
  team_id = "9007169192"
  url = "https://api.clickup.com/api/v2/team/" + team_id 
  headers = {"Authorization": params["CLICKUP_API_TOKEN"]}

  response = requests.get(url, headers=headers) # type: ignore

  data = response.json()
  print(data)

def create_task(name_task:str, description_task:str, priority:int = 1, print_message:bool = True) -> None:

  params = dotenv_values("data/.env")
  list_id = params["CLICKUP_LIST_ID"]
  url = "https://api.clickup.com/api/v2/list/" + str(list_id) + "/task"
  today = datetime.now(timezone.utc).replace(tzinfo=timezone.utc).timestamp() * 1000

  query = {
    "custom_task_ids": "true",
    "team_id":  params["CLICKUP_TEAM_ID"]
  }

  payload = {
    "name": name_task,
    "description": description_task,
    "assignees": [
      users_id["Cleiton"],
      users_id['Claudinei']
    ],
    "priority": priority,
    "due_date": today,
    "due_date_time": False,
    "start_date": today,
    "start_date_time": False,
    "notify_all": True,
    "parent": None,
    "links_to": None,
    "check_required_custom_fields": True,
  }

  headers = {
    "Content-Type": "application/json",
    "Authorization": params["CLICKUP_API_TOKEN"]
  }

  response = requests.post(url, json=payload, headers=headers, params=query)

  data = response.json()

  if print_message:
    print(data)
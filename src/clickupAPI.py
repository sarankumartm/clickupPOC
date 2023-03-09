import json
import requests
from values import API_KEY, CLICKUP_ENDPOINT, CONTENT_TYPE
import datetime
import re


# All the members associated with list_id are extracted here.
def list_members(list_id):
    try:
        # Endpoint to fetch all the members in a list_id.
        url = f"{CLICKUP_ENDPOINT}/list/{list_id}/member"
        headers = {
            'Authorization': API_KEY  # Fetching from values.py
        }
        response = requests.request("GET", url, headers=headers, data={})
        response_json = json.loads(response.text)
        members = [str(response_json["members"][i]["id"])
                   for i in range(len(response_json["members"]))]
        # Once after extracting all the members returing the array back to folder_extractor function.
        return members
    except Exception as E:
        return {
            "Message": f"Error occured in list member extractor - {E}"
        }


# All the folder_id and its associated list_ids are fetched here.
def folder_extractor(team_id):
    try:
        # Extracting all the folders inside one space.
        url = f'{CLICKUP_ENDPOINT}/space/{team_id}/folder'
        headers = {
            'Content-Type': CONTENT_TYPE,
            'Authorization': API_KEY  # Fetching from values.py
        }
        response = requests.request("GET", url, headers=headers, data="")
        # Recieving the extracts in string format so loading them into JSON.
        response_json = json.loads(response.text)
        # Extracting all the list_id inside every folder.
        # Getting all the member_id's associated with the list_id by calling, list_members function.
        folders_lists_members = sum([sum([list_members(response_json["folders"][i]["lists"][j]["id"]) for j in range(len(response_json["folders"][i]["lists"]))], [])
                                    for i in range(len(response_json["folders"]))], [])
        # Removing all the duplicate member_ids fetched.
        member_ids = [*set(folders_lists_members)]
        # Storing all the folder_id's and their names in dictionary.
        folder_id_name = {response_json["folders"][folders]["id"]: response_json["folders"][folders]["name"] for folders in range(
            len(response_json["folders"]))}
        # Storing all the list id and their names in dictionary.
        list_id_name = {}
        for i in range(len(response_json["folders"])):
            for j in range(len(response_json["folders"][i]["lists"])):
                list_id_name[response_json["folders"][i]["lists"][j]
                             ["id"]] = response_json["folders"][i]["lists"][j]["name"]

        return member_ids, folder_id_name, list_id_name

    except Exception as E:
        return {
            "Message": f"Error occured in folder extractor - {E}"
        }


# Epoch to timestamp conversion happens in this fn.
def epoch_timestamp(epoch_millisecond):
    return datetime.datetime.fromtimestamp(int(epoch_millisecond) / 1000).isoformat()


# Regular expression to split project code from project title.
def project_code(title):
    try:
        val = re.search(r"(?<=PR-).*?(?= )", title).group(0)
        return (val)
    except AttributeError as error:
        return ("Null")

# Millisecond to hour convertor - used for duration tracked.


def millisecond_hour_convertor(millis):
    seconds = (millis/1000) % 60
    seconds = int(seconds)
    minutes = (millis/(1000*60)) % 60
    minutes = int(minutes)
    hours = (millis/(1000*60*60)) % 24
    return ("%d:%d:%d" % (hours, minutes, seconds))

# All the task done inside a workspace are fetched are extracted in this fn.


def task_extractor(team_id, work_space_id, member_ids, start_date, end_date, folder_id_name, list_id_name):
    try:
        url = f"{CLICKUP_ENDPOINT}/team/{team_id}/time_entries"
        query = {
            "start_date": '',  # Dynamic value can be feeded.
            "end_date_date": '',  # Dynamic value can be feeded.
            "assignee": ','.join(member_ids),
            "space_id": str(work_space_id)
        }
        headers = {
            'Content-Type': CONTENT_TYPE,
            'Authorization': API_KEY  # Fetching from values.py
        }
        response = requests.get(url, headers=headers, params=query)
        data = response.json()
        # Creating an object that contains all the required fields and appending them to task list.
        tasks = [{"Project Code": project_code(folder_id_name[data["data"][i]["task_location"]["folder_id"]] if "task_location" in data["data"][i].keys() else "Null"),
                  "User Email address": data["data"][i]["user"]["email"],
                  # Doing all date and time related operations here.
                  "Entered date": epoch_timestamp(data["data"][i]["at"]),
                  "Start Date":epoch_timestamp(data["data"][i]["start"]),
                  "End Date": epoch_timestamp(data["data"][i]["end"]),
                  "Time Tracked":millisecond_hour_convertor(int(data["data"][i]["duration"])),
                  # There is chance for no tasks so having some validation over here, incase of no task "Null" is returned.
                  "Space ID": data["data"][i]["task_location"]["space_id"] if "task_location" in data["data"][i].keys() else "Null",
                  "Folder Name": folder_id_name[data["data"][i]["task_location"]["folder_id"]] if "task_location" in data["data"][i].keys() else "Null",
                  "List Name": list_id_name[data["data"][i]["task_location"]["list_id"]] if "task_location" in data["data"][i].keys() else "Null",
                  "Task Name": data["data"][i]["task"]["name"] if data["data"][i]["task"] != "0" else "0",
                  "Task ID": data["data"][i]["task"]["id"] if data["data"][i]["task"] != "0" else "0"}
                 for i in range(len(data["data"]))]
        # Once final tasks are extracted they're returned.
        return tasks

    except Exception as E:
        return {
            "Message": f"Error occured in folder extractor - {E}"
        }

from clickupAPI import folder_extractor, task_extractor
from values import *
import pprint


# Main function.
def main():
    try:
        # In this all_tasks, we store all the tasks of the given workspaces.
        all_tasks = []
        team_id = TEAM_ID
        # Looping through each workspace.
        for work_space_id in WORKSPACE_ID:
            # Incase tasks needed for a specific time interval.
            start_date = ''
            end_date = ''
            # Fetching all the member_ids associated with a list.
            member_ids, folder_id_name, list_id_name, space_id_name = folder_extractor(
                work_space_id)
            if len(member_ids) == 0:
                return "Empty space / No members found !"
            # Fetching all the tasks.
            tasks = task_extractor(team_id, work_space_id,
                                   member_ids, start_date, end_date, folder_id_name, list_id_name, space_id_name)
            # Adding tasks of each workspace to all_tasks.
            print(len(tasks))
            all_tasks.extend(tasks)
        # Returning the final tasks.
        # for i in all_tasks:
            # print("")
            # pprint.pprint(i)
        print(len(all_tasks))
        return all_tasks
    except Exception as E:
        return {
            "Message": f"Error occured - {E}"
        }


if __name__ == "__main__":
    main()

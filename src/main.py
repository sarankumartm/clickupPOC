from clickupAPI import folder_extractor, task_extractor
from values import *
import pprint


# Main function.
def main():
    try:
        team_id = TEAM_ID
        work_space_id = WORKSPACE_ID  # This can be made dynamic.
        # Incase tasks needed for a specific time interval.
        start_date = ''
        end_date = ''
        # Fetching all the member_ids associated with a list.
        member_ids, folder_id_name, list_id_name = folder_extractor(
            work_space_id)
        if len(member_ids) == 0:
            return "Empty space / No members found !"
        # Fetching all the tasks.
        tasks = task_extractor(team_id, work_space_id,
                               member_ids, start_date, end_date, folder_id_name, list_id_name)
        # Returning the final tasks
        for i in tasks:
            print("")
            pprint.pprint(i)
        return tasks
    except Exception as E:
        return {
            "Message": f"Error occured - {E}"
        }


if __name__ == "__main__":
    main()

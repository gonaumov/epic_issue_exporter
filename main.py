import csv
import os

from jira import JIRA

REPORT_CSV_FILE_NAME = 'epic_report.csv'

jira_server = os.getenv('JIRA_SERVER')
token_auth = os.getenv('TOKEN_AUTH')
epic_key = os.getenv('EPIC_KEY')

jira_options = {'server': jira_server}

jira = JIRA(options=jira_options, token_auth = token_auth)

# Function to create a link to an issue
def issue_link(issue_key):
    return f"{jira_server}browse/{issue_key}"

# Function to convert original estimate to hours
def convert_to_hours(estimate):
    if estimate:
        time_units = {'w': 40, 'd': 8, 'h': 1}
        total_hours = 0
        for unit in time_units:
            if unit in estimate:
                value = int(estimate.split(unit)[0])
                total_hours += value * time_units[unit]
                estimate = estimate.split(unit)[1]
        return total_hours
    return None

def export_issues_in_epic():
    issues_in_epic = jira.search_issues(f'"Epic Link" = {epic_key}')

    # Create the report
    report = []

    for current_issue in issues_in_epic:
        issue_data = {
            'key': current_issue.key,
            'summary': current_issue.fields.summary,
            'original_estimate': current_issue.fields.timetracking.originalEstimate,
            'original_estimate_hours': convert_to_hours(current_issue.fields.timetracking.originalEstimate),
            'description': current_issue.fields.description,
            'link': issue_link(current_issue.key),
            'subtasks': []
        }

        # Fetch subtasks for the issue
        for subtask_in_current_issue in current_issue.fields.subtasks:
            subtask_details = jira.issue(subtask_in_current_issue.key)
            subtask_data = {
                'key': subtask_in_current_issue.key,
                'summary': subtask_details.fields.summary,
                'description': subtask_details.fields.description,
                'link': issue_link(subtask_in_current_issue.key)
            }
            issue_data['subtasks'].append(subtask_data)

        report.append(issue_data)

    with open(REPORT_CSV_FILE_NAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['Issue Key', 'Issue type', 'Summary', 'Original Estimate', 'Original Estimate (Hours)', 'Subtask Parent Issue Key', 'Link'])
        for issue in report:
            writer.writerow(
                [issue['key'], 'Task', issue['summary'], issue['original_estimate'], issue['original_estimate_hours'], '', issue['link']])
            if len(issue['subtasks']) > 0:
                for subtask in issue['subtasks']:
                    writer.writerow(
                        [subtask['key'], 'Sub task', subtask['summary'], '', 0, issue['key'], subtask['link']])
    print(f"All done! Please check {REPORT_CSV_FILE_NAME} file.")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    export_issues_in_epic()
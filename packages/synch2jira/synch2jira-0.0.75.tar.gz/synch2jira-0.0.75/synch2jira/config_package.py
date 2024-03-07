def config_package():
    package_dir = "/home/ibtihell/PycharmProjects/sync2jira_package/synch2jira"
    with open('configurations.py', 'w') as fichier_config:
        fichier_config.write(f"""
import logging
import os
from requests.auth import HTTPBasicAuth \n
username = "BillGates" 
#Api token de jira 
api_token = "TATT3xFfGF0nqgTV-RGN17B9CmizmQD0Mmr5ZY-pU0t8TjTzz0lyX0MNJ0XoNdKNy_t4eq9Is3Gw51Mta-kHF0XrEjKUANWzJM1XpRqS_-wSssC"

auth = HTTPBasicAuth(username, api_token)

jira_url_base = "https://example.atlassian.net/"
project_key = "90009"
key_issue_type = "10005"
s1_id_in_jira = "customfield_10054"

statusesS1 = ["status1", "status2", "status3", "status4"]
jiraStatusName = ["To Do", "Pret", "In Progress", "Done"]
jiraTransition = ["En attente", "Pret", "en cours", "Qualifications"]


module_to_use = "synch2jira.implementation_issue_S3"
class_to_use = "IssueImplementationS3"
""")


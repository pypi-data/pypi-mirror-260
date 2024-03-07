import requests
from requests.auth import HTTPBasicAuth

import config


def get_config_data():
    table = {}
    with open(config.config_file, 'r') as file:
        for line in file:
            if '=' in line:
                parts = line.split("=", 1)
                titre = parts[0].strip()
                valeur = parts[1].strip()
                if valeur.startswith('"') or valeur.endswith('"'):
                    valeur = valeur[1:-1]
                table[titre] = valeur
    return table


def update_data_jira(username, jira_url_base, api_token):
    with open(config.config_file, 'r') as file:
        lines = file.readlines()

    with open(config.config_file, 'w') as file:
        for line in lines:
            if line.startswith("username ="):
                file.write(f"username = \"{username}\"\n")
            elif line.startswith("jira_url_base ="):
                file.write(f"jira_url_base = \"{jira_url_base}\"\n")
            elif line.startswith("api_token ="):
                file.write(f"api_token = \"{api_token}\"\n")
            else:
                file.write(line)


def update_data_cles(project_key, key_issue_type, s1_id_in_jira):
    with open(config.config_file, 'r') as file:
        lines = file.readlines()

    with open(config.config_file, 'w') as file:
        for line in lines:
            if line.startswith("project_key ="):
                file.write(f"project_key = \"{project_key}\"\n")
            elif line.startswith("key_issue_type ="):
                file.write(f"key_issue_type = \"{key_issue_type}\"\n")
            elif line.startswith("s1_id_in_jira ="):
                file.write(f"s1_id_in_jira = \"{s1_id_in_jira}\"\n")
            else:
                file.write(line)


def update_data_synch2jira(module_to_use, class_to_use, database_file):
    with open(config.config_file, 'r') as file:
        lines = file.readlines()

    with open(config.config_file, 'w') as file:
        for line in lines:
            if line.startswith("module_to_use ="):
                file.write(f"module_to_use = \"{module_to_use}\"\n")
            elif line.startswith("class_to_use ="):
                file.write(f"class_to_use = \"{class_to_use}\"\n")
            elif line.startswith("database_file ="):
                file.write(f"database_file = \"{database_file}\"\n")
            else:
                file.write(line)


def update_data_status(statusesS1, jiraStatusName, jiraTransition):
    with open(config.config_file, 'r') as file:
        lines = file.readlines()

    with open(config.config_file, 'w') as file:
        for line in lines:
            if line.startswith("statusesS1 ="):
                file.write(f"statusesS1 = \"{statusesS1}\"\n")
            elif line.startswith("jiraStatusName ="):
                file.write(f"jiraStatusName = \"{jiraStatusName}\"\n")
            elif line.startswith("jiraTransition ="):
                file.write(f"jiraTransition = \"{jiraTransition}\"\n")
            else:
                file.write(line)

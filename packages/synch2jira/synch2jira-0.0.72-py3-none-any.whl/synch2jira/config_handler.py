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


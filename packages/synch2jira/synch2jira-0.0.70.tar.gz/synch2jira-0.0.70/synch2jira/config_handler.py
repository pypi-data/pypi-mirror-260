import requests
from requests.auth import HTTPBasicAuth

import config


def get_config_data():
    table = {}
    with open(config.config_file, 'r') as file:
        for line in file:
            if '=' in line:
                parts = line.split("=")
                titre = parts[0].strip()
                valeur = parts[1].strip()
                if valeur.startswith('"') or valeur.endswith('"'):
                    valeur = valeur[1:-1]
                table[titre] = valeur
    return table


def get_config_data_jira():
    data = get_config_data()
    return data.get('username'), data.get('api_token'), data.get('jira_url_base')


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


if __name__ == '__main__':
    print(get_config_data())

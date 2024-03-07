import logging
from distutils import config
from synch2jira.synchronisation import Synchronisation
from synch2jira.implementation_issue_S1 import IssueImplementationS1
from synch2jira.implementation_issue_S2 import IssueImplementationS2

logging.basicConfig(filename=config.log_file, level=logging.INFO, format=config.log_format)
status_dict_S1_to_S2 = {"status1": "To Do", "status2": "Pret", "status3": "In Progress", "status4": "Done"}
status_dict_S1_to_S2 = {"En attente": "status1", "Pret": "status2", "En cours": "status3", "Qualifications": "status4"}


class ImplementationSynchonisationS1(Synchronisation):
    pass

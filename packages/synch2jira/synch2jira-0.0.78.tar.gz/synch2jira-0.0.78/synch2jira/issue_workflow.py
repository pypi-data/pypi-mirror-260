from dataclasses import dataclass
from datetime import datetime
from statistics import mean
from synch2jira.implementation_issue_wokflow import IssueWokflow

@dataclass
class WorkFlow():
    issueKey:str
    
    
    def get_duration_between_two_state(issue_key,state1,state2):
        if IssueWokflow.did_issue_have_state(issue_key,state1) and IssueWokflow.did_issue_have_state(issue_key,state2):
            worflow1 = IssueWokflow.find_by(issueKey = issue_key,status = state1)[0]
            worflow2 = IssueWokflow.find_by(issueKey = issue_key,status = state2)[0]
            date1 = WorkFlow.convert_str_time_to_unix(worflow1.from_time) 
            date2 = WorkFlow.convert_str_time_to_unix(worflow2.from_time)
            date3 = WorkFlow.convert_str_time_to_unix(worflow2.to_time)
            return [issue_key, worflow2.from_time,worflow1.from_time,date1-date2]
        else:
            pass
        
    def get_all_duration_between_to_state(state1,state2,issue_list):            
        return [WorkFlow.get_duration_between_two_state(issue,state1,state2) for issue in issue_list]
        
    def get_mean_duration(state1,state2,issue_list):
        return mean(WorkFlow.get_duration_between_two_state(state1,state2,issue_list))
        
    def is_in_state(state):
        return False
    def get_all_issues_with_state(cls,state):
        return []
    


    def get_worflow_history():
       pass
    def csv_export(cls,state1,state2):
        pass
    @staticmethod
    def convert_str_time_to_unix(time):
            timestamp_format = "%Y-%m-%dT%H:%M:%S.%f%z"
            element = datetime.strptime(time,timestamp_format)
            timestamp = datetime.timestamp(element)
            return timestamp
    
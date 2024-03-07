from dataclasses import dataclass
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String,Integer,create_engine,DateTime,and_,text,desc
import config
from datetime import datetime, timezone
import csv
import requests
import json
import time

from synch2jira.implementation_issue_S2 import IssueImplementationS2

Base = declarative_base()
engine = create_engine(config.workflow_database_file)
Session = sessionmaker(bind = engine)
session = Session()
Base.metadata.create_all(engine)

@dataclass
class IssueWokflow(Base):
    __tablename__ = 'issue_worflow'
    id = Column(Integer,autoincrement=True,primary_key=True)
    issueKey = Column(String)
    status = Column(String)
    updated = Column(DateTime)
    from_time = Column(String)
    to_time = Column(String)

    def __init__(self,issueKey,status,updated,from_time,to_time):
        self.from_time = from_time
        self.issueKey = issueKey
        self.updated = updated
        self.status = status
        self.to_time = to_time



    def get_workflow_history(self):
        return self.all()
    
    def workflow_csv_export(self):
        return True
    
    @staticmethod
    def update_last_updated(issue_key,updated):
        issue = IssueWokflow.find_by_issueKey(issue_key)
        issue.updated = updated
        issue.update()

        return None
    
    def fill_issue_workflow_bdd():
        print("tring to fill bdd ")
        print("tring to create tables")
        IssueWokflow.create_all_tables()
        print("creation went succesull")

        jira_columns = config.jiraTransition
        jira_issues_list = [issue.key for issue in IssueImplementationS2.all()]
        #jira_issues_list = ["KAN-1585","KAN-99"]
        #print(f'liste des cles {jira_issues_list}')
        for issue_key in jira_issues_list:
            for status in jira_columns:
                from_time,to_time = IssueWokflow.get_workflow_v2(issue_key,status)
                workflow = IssueWokflow(issue_key,status,datetime.now(),from_time,to_time)
                workflow.save()
        print("end of filling")

    def did_issue_have_state(issue_key,state):
        ### verifier updated 
        workflow_list = IssueWokflow.find_by(issueKey = issue_key,status = state)
        for workflow in workflow_list:
            if workflow.from_time and workflow.to_time:
                print("oks",issue_key)
                return True        
        return False
    
    def synchronize_data_with_jira():
        jira_columns = config.jiraTransition
        issue_in_jira_list = IssueImplementationS2.all()
        #issue_in_jira_list = [IssueImplementationS2.find_by_id('KAN-99'),IssueImplementationS2.find_by_id('KAN-3')]
        #workflow_list = IssueWokflow.all()
        for issue_jira in issue_in_jira_list:
            workflow = IssueWokflow.find_by_id(issue_jira.key)[0]
            print(issue_jira.key,workflow.updated,issue_jira.updated)
            #print(type(workflow.updated),type(issue_jira.updated))
            is_updated_on_date = IssueWokflow.compare_str_dates(workflow.updated,issue_jira.updated)
                 
            if not is_updated_on_date:
                for status in jira_columns:
                    from_time,to_time = IssueWokflow.get_workflow_v2(issue_jira.key,status)
                    workflow = IssueWokflow.find_by(issueKey = issue_jira.key,status = status)[0]
                    workflow.from_time = from_time
                    workflow.to_time = to_time
                    workflow.update()
                    print(workflow.issueKey)
                    #workflow.save()
            


    def compare_str_dates(date1,date2):
        date1 = date1.replace(tzinfo=timezone.utc)
        date2 = datetime.strptime(date2, "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=timezone.utc)
        print(f'date 1 {date1} , date 2 {date2}')
        if date1 > date2:
            #KAN-17 2024-03-05 09:13:40.998417 2024-03-05T11:27:28.959+0100
            #KAN-99 2024-03-05 11:06:19.485890 2024-03-05T11:27:29.733+0100
            print("La date worflow est plus grande que la date jira.")
            return True
        
        print("La  date  jira est plus grande que la  date woakflow.")
        return False
       


        
    
    @staticmethod
    def get_workflow(issue_key,status):
        from_time = None
        to_time = None
        history_url = f"{config.jira_url_ticket}{issue_key}/changelog"
        history_response = requests.get(history_url, auth=config.auth)
        if history_response.status_code != 200:
                return False
        history_data = history_response.json()
        histories = history_data['values']
        for history in histories:
            created = history['created']
            items = history['items']
            for item in items:
                field = item['field']
                if field == "status":
                    if item['fromString'] == status:
                        from_time = created
                    if item['toString'] == status:
                        to_time = created
        print("V1",from_time,to_time)
        return from_time,to_time
    
    def get_workflow_v2(issue_key,status):
        from_time = []
        to_time = []
        history_url = f"{config.jira_url_ticket}{issue_key}/changelog"
        history_response = requests.get(history_url, auth=config.auth)
        if history_response.status_code != 200:
                return False
        history_data = history_response.json()
        histories = history_data['values']
        for history in histories:
            created = history['created']
            items = history['items']
            for item in items:
                field = item['field']
                if field == "status":
                    if item['fromString'] == status:
                        from_time.append(created)
                    if item['toString'] == status:
                        to_time.append(created)

        min_from_time = None if from_time == [] else min(from_time) 
        max_to_time =None if to_time == [] else  max(to_time)
        print(f'from rtimes , {min_from_time},to time {max_to_time}')
        return min_from_time,max_to_time

    

    def save_result_in_csv(result, entete):
        filename = "workflow_time.csv"
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            
            writer.writerow(entete)
            
            # Parcourir la liste result et ajouter une ligne pour chaque élément
            for row in result:
                print(row)
                writer.writerow(row)
                
        print(f"Les données ont été écrites dans {filename}")

    @staticmethod
    def create(**kwargs):  # avec les argument on creee un objet et on le save
        workflow = IssueWokflow(**kwargs)
        session.add(workflow)
        session.commit()
        return workflow

    @staticmethod
    def create_all_tables():
        Base.metadata.create_all(engine)

    @staticmethod
    def new(**kwargs):  # avec les argument on creee un objet sans le save
        return IssueWokflow(**kwargs)

    @staticmethod
    def all():
        return session.query(IssueWokflow).all()

    def save(self):
        session.add(self)
        session.commit()
        return self

    def get(self):
        return session.query(IssueWokflow).filter(
            and_(IssueWokflow.issueKey == self.issueKey,IssueWokflow.status == self.status)).first()

    @staticmethod
    def first():
        return session.query(IssueWokflow).first()

    @staticmethod
    def last():
        return session.query(IssueWokflow).order_by(desc(IssueWokflow.issueKey)).first()

    @staticmethod
    def find_by(**kwargs):
        return session.query(IssueWokflow).filter_by(**kwargs).all()

    @staticmethod
    def find_by_id(key):
        return session.query(IssueWokflow).filter_by(issueKey=key).all()

    @staticmethod
    def update(instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        session.commit()

    def update(self):
        self.updated =  datetime.now()
        session.merge(self)
        session.commit()

    @staticmethod
    def update_all(**kwargs):
        session.query(IssueWokflow).update(kwargs)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def delete_all():
        session.execute(text("DELETE FROM worflow"))
        session.commit()
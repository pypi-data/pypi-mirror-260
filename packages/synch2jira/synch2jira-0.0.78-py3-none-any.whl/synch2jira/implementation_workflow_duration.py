from dataclasses import dataclass
from synch2jira.workflow_duration import WorkFlowDuration
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, create_engine, DateTime, and_, text, Integer, desc
from sqlalchemy.orm import declarative_base

import config

Base = declarative_base()
engine = create_engine(config.workflow_database_file)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

@dataclass 
class ImplementationWorflowDuration(Base,WorkFlowDuration):
    __tablename__ = 'worflows'

    key = Column(String, primary_key= True)
    # Issue = Column(String)
    # Pret_to_En_attente = Column(String)
    # Pret_to_en_cours = Column(String)
    # Pret_to_en_cours = Column(String)
    # Pret_to_Qualifications = Column(String)
    # En_attente_to_en_cours = Column(String)
    # En_attente_to_Qualifications = Column(String)
    # en_cours_to_Qualifications = Column(String)


    # Définition dynamique des colones SQLAlchemy en fonction du nombre de la liste 
    @classmethod
    def create_dynamic_columns(cls, workflow_columns):
        #setattr(cls,"Ussue",Column(String, primary_key=True))
        for column in workflow_columns:
            setattr(cls, column, Column(String))
        setattr(cls,"Updated",Column(DateTime))

    def r__init___(self, *args, **kwargs):
        for i, arg in enumerate(args):
            setattr(self, f'column_{i}', Column(String, default=arg))

    def r__init__(self, **kwargs):
        for key, value in kwargs.items():
            print(f"Key, {key}, Value, {value}")
            setattr(self, key, Column(String, default=value))
    @staticmethod
    def create(**kwargs):  # avec les argument on creee un objet et on le save
        workflow = ImplementationWorflowDuration(**kwargs)
        session.add(workflow)
        session.commit()
        return workflow

    @staticmethod
    def create_all_tables():
        Base.metadata.create_all(engine)

    @staticmethod
    def new(**kwargs):  # avec les argument on creee un objet sans le save
        return ImplementationWorflowDuration(**kwargs)

    @staticmethod
    def all():
        return session.query(ImplementationWorflowDuration).all()

    def save(self):
        retour = Base.metadata.create_all(engine)
        print(f"retour de create == {retour}")
        #self.updated = datetime.now()
        print(datetime.now())
        session.add(self)
        session.commit()
        return self

    def get(self):
        return session.query(ImplementationWorflowDuration).filter(
            and_(ImplementationWorflowDuration.id == self.id)).first()

    @staticmethod
    def first():
        return session.query(ImplementationWorflowDuration).first()

    @staticmethod
    def last():
        return session.query(ImplementationWorflowDuration).order_by(desc(ImplementationWorflowDuration.id)).first()

    @staticmethod
    def find_by(**kwargs):
        return session.query(ImplementationWorflowDuration).filter_by(**kwargs).all()

    @staticmethod
    def find_by_id(key):
        return session.query(ImplementationWorflowDuration).filter_by(key=key).first()

    @staticmethod
    def update(instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        session.commit()

    def update(self):
        self.updated = datetime.now()
        session.merge(self)
        session.commit()

    @staticmethod
    def update_all(**kwargs):
        session.query(ImplementationWorflowDuration).update(kwargs)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

    @staticmethod
    def delete_all():
        session.execute(text("DELETE FROM worflow"))
        session.commit()

    
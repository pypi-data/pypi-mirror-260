import synch2jira.setup_files
from synch2jira.historique import HistoriqueSynchronisation
import config


class ImplementationHistorique(HistoriqueSynchronisation):

    def save_synchronisation(self):
        try:
            with open(synch2jira.setup_files.history_file, "a") as history:
                history.write(self.date + "," + self.synchro_message + "\n")
                history.close()
                return True
        except Exception as e:
            print(e)
            return False

import logging
import os

import synch2jira.setup_files
from synch2jira.implementation_issue_S1 import IssueImplementationS1
from synch2jira.implementation_issue_S2 import IssueImplementationS2
from synch2jira.implementation_table_correpondance_key_id import verifier_existence_id, save_correspondance_table, \
    rebuild_correspondence_table, get_correspondence_table, \
    save_correspondence_dict

logging.basicConfig(filename=synch2jira.setup_files.log_file, level=logging.INFO, format=synch2jira.setup_files.log_format)


class Synchronisation:
    issue1 = IssueImplementationS1.issue1_factory(summary='', description='', updated=None, status='')

    @staticmethod
    def synchronisation_S2_S1():
        if not (os.path.exists(synch2jira.setup_files.table_correspondance_file)) or os.path.getsize(
                synch2jira.setup_files.table_correspondance_file) == 0:
            print("try to rebuils correspondence table ")
            rebuild_correspondence_table()
        issues_in_S2 = IssueImplementationS2.all_filtre_id_et_updated()
        for issue_in_S2 in issues_in_S2:
            miror_S1_de_S2 = issue_in_S2.miror
            if miror_S1_de_S2 is None:
                issue_complet_S2 = issue_in_S2.get()
                issue_S2_convertie_en_S1 = IssueImplementationS1.convertirS_enS_(issue_complet_S2)
                issue_complet_S2.miror = issue_S2_convertie_en_S1.save()
                issue_complet_S2.update()
                logging.info(f"Ajout du ticket N°{issue_complet_S2.key} dans S1")

            # elif miror_S1_de_S2 and Issue.date_S1_entre_date_derniere_synchro_et_date_S2(miror_S1_de_S2.updated,
            #                                                                           issue_in_S2.updated):
            #     issue_complet_S2_convertie_en_S1.update()
            #     logging.info(f"Modification du ticket N°{issue_in_S2.key} dans S1")

            # issue_in_S1 = Issue.trouver(issue_in_S2, issues_in_S1)
            # issue_to_save_or_update = IssueImplementationS1.convertirS_enS_(issue_in_S2.get())
            # if issue_in_S1 is None:
            #     issue_to_save_or_update.save()
            #     logging.info(f"Ajout du ticket N°{issue_in_S2.key} dans S1")
            #     # Changer fonction date_S1_entre_date_derniere_synchro_et_date_S2 en utilisant mirror
            # elif issue_in_S1 and Issue.date_S1_entre_date_derniere_synchro_et_date_S2(issue_in_S1.updated,
            #                                                                           issue_in_S2.updated):
            #     issue_to_save_or_update.update()
            #     logging.info(f"Modification du ticket N°{issue_in_S2.key} dans S1")

    @staticmethod
    def synchronisation_S1_S2():  # Créer a partir de S1 tout les S2
        issues_in_S1 = IssueImplementationS1.all_filtre_id_et_updated()
        for issue_in_S1 in issues_in_S1:
            if not verifier_existence_id(issue_in_S1.id):
                issue_complet_S1 = IssueImplementationS1.find_by_id(issue_in_S1.id)
                correspondance_S2 = IssueImplementationS2.convertirS_enS_(issue_complet_S1)
                correspondance_S2.miror = issue_in_S1
                key = correspondance_S2.save()
                save_correspondance_table(key, issue_in_S1.id)

    @staticmethod
    def synchronisation_S1_S2_v2():
        if not (os.path.exists(synch2jira.setup_files.table_correspondance_file)) or os.path.getsize(
                synch2jira.setup_files.table_correspondance_file) == 0:
            print("try to rebuils correspondence table ... ")
            rebuild_correspondence_table()
            print("end of the construction ...")
        table = get_correspondence_table()
        table_id_list = table.values()
        issue = IssueImplementationS1.issue1_factory("", "", None, "")
        issue_list = issue.all()
        new_correspondences = {}
        for issue in issue_list:
            if str(issue.id) not in table_id_list:
                miror = IssueImplementationS2(summary=issue.summary, description=issue.description, status=issue.status)
                miror.miror = issue
                key = miror.save()
                if len(key) > 10:
                    print("error  ", key)
                    print("issue ====", issue)
                    print("idd ===", issue.id)
                    print("mirror ===", miror)
                    break
                new_correspondences[key] = str(issue.id)
        save_correspondence_dict(new_correspondences)


if __name__ == "__main__":
    Synchronisation.synchronisation_S2_S1()

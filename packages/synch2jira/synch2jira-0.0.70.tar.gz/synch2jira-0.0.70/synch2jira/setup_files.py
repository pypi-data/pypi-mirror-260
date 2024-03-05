import os

main_directory = os.path.dirname(os.path.abspath(__file__))


log_file = main_directory + "/log/file.log"
log_format = '%(asctime)s - %(levelname)s - %(message)s'
table_correspondance_file = main_directory + "/files/correspondance_table.json"
history_file = main_directory + "/files/history.txt"
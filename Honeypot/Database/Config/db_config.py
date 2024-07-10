import json
import os

# Dynamically get path to json
current_directory = os.path.dirname(os.path.abspath(__file__))
json_file = os.path.join(current_directory, 'db_config.json')

# Open file
with open(json_file) as config_file:
    config = json.load(config_file)

# load information from the file
database_config = config['database_config']  
table_names = config['table_names']

# Extract the information form the files
db_host = database_config['db_host']
db_user = database_config['db_user']
db_port = database_config['db_port']
db_passwd = database_config['db_passwd']
db_name = database_config['db_name']

table_1 = table_names['table_1']
table_2 = table_names['table_2']
table_3 = table_names['table_3']
table_4 = table_names['table_4']
table_5 = table_names['table_5']
table_6 = table_names['table_6']
table_7 = table_names['table_7']
table_8 = table_names['table_8']

tables_to_check = config['tables_to_check']
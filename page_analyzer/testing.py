from page_analyzer.validate import is_valid
from page_analyzer.connected import connect_to_db



max_query = f'''SELECT MAX(id) FROM urls'''

max_id = connect_to_db(max_query)
print(max_id[0][0])
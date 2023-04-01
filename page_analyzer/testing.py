from page_analyzer.connected import connect_to_db

max_query = '''SELECT MAX(id) FROM urls'''

max_id = connect_to_db(max_query)
print(max_id[0][0])

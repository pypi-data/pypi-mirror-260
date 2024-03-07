from hashquery import *
from hashquery.hashboard_api.project_importer import ProjectImporter

connection = ProjectImporter().data_connection_by_alias("CONNECTION_NAME")

table_model = Model().with_data_source(connection, table("TABLE_NAME"))

count_model = table_model.aggregate(groups=[], measures=[count()])

results = run(count_model)
print(results.df)

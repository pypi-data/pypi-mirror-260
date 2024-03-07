from hashquery import *
from hashquery.hashboard_api.project_importer import ProjectImporter

connection = ProjectImporter().data_connection_by_alias("CONNECTION_NAME")

table_model = Model().with_data_source(connection, table("TABLE_NAME"))

top_counts_model = (
    table_model.aggregate(
        groups=[column("COLUMN_NAME")],
        measures=[count()],
    )
    .sort(column("count"))
    .take(3)
)

results = run(top_counts_model)
print(results.df)

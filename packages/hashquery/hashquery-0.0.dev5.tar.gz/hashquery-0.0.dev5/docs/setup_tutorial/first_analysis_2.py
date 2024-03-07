from hashquery import *
from hashquery.hashboard_api.project_importer import ProjectImporter

connection = ProjectImporter().data_connection_by_alias("CONNECTION_NAME")

table_model = (
    Model()
    .with_data_source(connection, table("TABLE_NAME"))
    .with_attribute(column("COLUMN_NAME").named("my_attribute"))
    .with_measure(count().named("my_measure"))
)

top_counts_model = (
    table_model.aggregate(
        groups=[_.my_attribute],
        measures=[_.my_measure],
    )
    .sort(_.my_measure)
    .take(3)
)

results = run(top_counts_model)
print(results.df)

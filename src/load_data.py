
from sqlalchemy import MetaData, Table
from sqlalchemy.dialects.postgresql import insert

def upsert_dataframe(df, table, conn):
    records = df.to_dict(orient="records")
    if not records:
        return

    stmt = insert(table).values(records)
    update_columns = {col.name: stmt.excluded[col.name] for col in table.columns if not col.primary_key}
    stmt = stmt.on_conflict_do_update(index_elements=[col.name for col in table.primary_key.columns],
                                      set_=update_columns,)
    conn.execute(stmt)

def load_idempotently(engine, instances_df, metrics_df):
    metadata = MetaData()

    with engine.begin() as conn:
        instances_table = Table("instances", metadata, schema="raw", autoload_with=conn,)
        metrics_table = Table("instance_metrics", metadata, schema="raw", autoload_with=conn,)

        upsert_dataframe(instances_df, instances_table, conn,)

        batch_size = 1000

        for start in range(0, len(metrics_df), batch_size):
            batch = metrics_df.iloc[start:start + batch_size]
            upsert_dataframe(batch, metrics_table, conn,)


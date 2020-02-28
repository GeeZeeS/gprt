from sqlalchemy import and_
from pandas import DataFrame, merge, date_range, concat, read_sql_query
from datetime import datetime, timedelta
from . models import WarehouseModel
from . import mongo, db, redis, scheduler, app
from os import environ


def main_job():
    # Check if DB is populated
    whm_count = WarehouseModel.query.count()
    if whm_count > 0:
        # Check if last_inserted date is stored
        last_date = redis.get("last_date").decode('utf-8')
        if last_date is None:
            # Get last inserted row in DB
            whm_last_date = WarehouseModel.query.order_by(
                WarehouseModel.created_at.desc()
            ).first()
            start_date = whm_last_date.created_at + timedelta(seconds=1)
        else:
            # Set start date from redis value
            start_date = datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=1)
        end_date = start_date + timedelta(seconds=299)
    else:
        # Get first row from mongo db
        start_date = mongo.db.mng_db['orders'].find({}).sort([("created_at", 1)]).limit(1)[0]['created_at']
        # Set max date to fetch
        end_date = datetime(2020, 1, 1)

    print(f"Populating Database from {start_date} to {end_date}")
    populate_data(start_date, end_date)
    redis.set("last_date", str(end_date).encode('utf-8'))  # set last_inserted date to redis


# Method for populating data within dates
def populate_data(start_date, end_date):
    df_created_orders = get_order_data('created_at', start_date, end_date)

    if not df_created_orders.empty:
        df_final = merge_data(df_created_orders)
        df_final.to_sql('warehouse', db.engine, if_exists='append', index_label='pk', index=False)
        print(f"{df_final.shape[0]} rows inserted")
    else:
        print("Empty Query, Sleeping for the next 5 minutes")
    updated_data(start_date, end_date)


# Method for updating values for updated data within dates
def updated_data(start_date, end_date):
    df_updated_orders = get_order_data('updated_at', start_date, end_date)
    if not df_updated_orders.empty:
        df_final = merge_data(df_updated_orders)
        df_warehouse = read_sql_query('SELECT * FROM warehouse', con=db.engine)

        # Check data that is duplicated, and let only unique one
        df_concat_updated_orders = concat([
            df_warehouse,
            df_final]).drop_duplicates(['updated_at'], keep=False, inplace=True)

        if df_concat_updated_orders is not None:
            df_concat_updated_orders.to_sql('warehouse', db.engine, if_exists='append', index_label='pk', index=False)
            print(f"{df_concat_updated_orders.shape[0]} rows updated between dates: {start_date} to {end_date}")


def merge_data(df_orders):
    df_users = DataFrame(mongo.db.mng_db['users'].find())  # Get Users dataframe
    df_final = merge(df_orders, df_users, on='user_id', how='left')  # Merge Dataframes Together
    df_final = df_final.drop(columns=['_id_x', '_id_y'])  # Remove ObjectID Columns
    df_final = column_rename(df_final)  # Rename Columns Based on the WarehouseModel model
    return df_final


# Get Filtered Order Data
def get_order_data(table_name, start_date, end_date):
    df_orders = DataFrame(mongo.db.mng_db['orders'].find(
        {
            f"{table_name}": {
                "$gte": str(start_date),
                "$lt": str(end_date)
            }
        }
    ).sort([(f"{table_name}", 1)]))
    return df_orders


def column_rename(df):
    df = df.rename(
        columns={
            'created_at_x': 'created_at',
            'updated_at_x': 'updated_at',
            'first_name': 'user_first_name',
            'last_name': 'user_last_name',
            'merchant_id': 'user_merchant_id',
            'phone_number': 'user_phone_number',
            'created_at_y': 'user_created_at',
            'updated_at_y': 'user_updated_at'
        }
    )
    return df


# Fix for scheduler to run once on startup
if not app.debug or environ.get('WERKZEUG_RUN_MAIN') == 'true':
    scheduler.start()
    scheduler.add_job(func=main_job, trigger="interval", seconds=300)

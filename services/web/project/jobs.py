from pandas import DataFrame, merge
from datetime import datetime, timedelta
from . models import WarehouseModel
from . import mongo, db, redis, scheduler, app
from os import environ


def main_job():
    whm_count = WarehouseModel.query.count()  # Get count of rows in DB
    if whm_count > 0:  # Check if DB is populated
        last_date = redis.get("last_date").decode('utf-8')  # Check if last_inserted date is stored
        if last_date is None:
            # Get last inserted date from db
            whm_last_date = WarehouseModel.query.order_by(
                WarehouseModel.created_at.desc()
            ).first()
            start_date = whm_last_date.created_at + timedelta(seconds=1)
        else:
            start_date = datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=1)
        end_date = start_date + timedelta(seconds=299)
    else:
        # Getting lowest Object from list
        orders_data_set = mongo.db.mng_db['orders'].find({}).sort([("created_at", 1)]).limit(1)

        # Setting start and end dates
        start_date = orders_data_set[0]['created_at']
        end_date = datetime(2020, 1, 1)

    print(f"Populating Database from {start_date} to {end_date}")  # Print info about populating data
    populate_data(start_date, end_date)  # write data to db
    redis.set("last_date", str(end_date).encode('utf-8'))  # set last_inserted date to redis


def populate_data(start_date, end_date):
    orders_data_set = mongo.db.mng_db['orders'].find(
        {
            "created_at": {
                "$gte": str(start_date),
                "$lt": str(end_date)
            }
        }
    ).sort([("created_at", 1)])  # Filter and get orders

    users_data_set = mongo.db.mng_db['users'].find({})  # Get Users

    # Dataframe Queries
    df_orders = DataFrame.from_records(orders_data_set)
    df_users = DataFrame.from_records(users_data_set)

    if not df_orders.empty:  # Check if Dataframe is empty
        df_final = merge(df_orders, df_users, on='user_id', how='left')  # Merge Dataframes Together
        df_final = df_final.drop(columns=['_id_x', '_id_y'])  # Remove ObjectID Columns
        df_final = column_rename(df_final)  # Rename Columns Based on the WarehouseModel model
        df_final.to_sql('warehouse', db.engine, if_exists='append', index=False)  # Write Dataframe to db
        print(f"{df_final.shape[0]} rows inserted")  # Output amount of rows inserted
    else:
        print("Empty Query, Sleeping for the next 5 minutes")  # Output that no data was found to populate


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

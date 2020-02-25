from pandas import DataFrame, merge
from datetime import datetime, timedelta
from . models import WarehouseModel
from . import mongo, db, redis, scheduler


def populate_data(start_date, end_date):
    # Filter orders data between dates
    orders_data_set = mongo.db.mng_db['orders'].find(
        {
            "created_at": {
                "$gte": str(start_date),
                "$lt": str(end_date)
            }
        }
    ).sort([("created_at", 1)])
    # Get Users Data
    users_data_set = mongo.db.mng_db['users'].find({})
    # Dataframe Queries
    df_orders = DataFrame.from_records(orders_data_set)
    df_users = DataFrame.from_records(users_data_set)
    # Check if Dataframe is empty
    if not df_orders.empty:
        # Merge Dataframes Together
        df_final = merge(df_orders, df_users, on='user_id', how='left')
        # Remove ObjectID Columns
        df_final = df_final.drop(columns=['_id_x', '_id_y'])
        # Rename Columns Based on the WarehouseModel model
        df_final = column_rename(df_final)
        # Write Dataframe to db
        df_final.to_sql('warehouse', db.engine, if_exists='append', index=False)
        # Output amount of rows inserted
        print(f"{df_final.shape[0]} rows inserted")
    else:
        # Output that no data was found within 5 minutes
        print("Empty Query, Sleeping for the next 5 minutes")


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


def main_job():
    # Get count of rows in DB
    whm_count = WarehouseModel.query.count()
    # Check if DB is populated
    if whm_count > 0:
        # If DB is populated check if last_inserted date is stored
        last_date = redis.get("last_date").decode('utf-8')
        if last_date is None:
            # If last_inserted date is not stored, get last inserted date from db, and start from there
            whm_last_date = WarehouseModel.query.order_by(
                WarehouseModel.created_at.desc()
            ).first()
            start_date = whm_last_date.created_at + timedelta(seconds=1)
            end_date = start_date + timedelta(seconds=299)
        else:
            # If last_inserted date is stored, get date and add 5 minutes
            start_date = datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=1)
            end_date = start_date + timedelta(seconds=299)

        print(f"Populating Database from {start_date} to {end_date}")

        # set last_inserted date to redis
        redis.set("last_date", str(end_date).encode('utf-8'))
        # write data to db
        populate_data(start_date, end_date)
    # If Database is not populated, import data till 1 January 2020
    else:
        # Getting Lowest Object from list
        orders_data_set = mongo.db.mng_db['orders'].find({}).sort([("created_at", 1)]).limit(1)
        start_date = orders_data_set[0]['created_at']

        # Setting highest Object to fetch
        end_date = datetime(2020, 1, 1)

        print(f"Populating Database from {start_date} to 1 January 2020")

        # set last_inserted date to redis
        redis.set("last_date", str(end_date).encode('utf-8'))
        # write data to db
        populate_data(start_date, end_date)


scheduler.start()
scheduler.add_job(func=main_job, trigger="interval", seconds=300)

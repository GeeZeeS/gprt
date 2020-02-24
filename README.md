# GoParrot Test

# Installation:
### Docker:
###### build a docker image
```
> docker-compose build
```
###### run a docker container
###### silent (no debug)
```
> docker-compose up -d
```
###### debug mode
```
> docker-compose up
```
###### Populate mongodb data from csv files
```
> docker-compose exec web python manage.py populate
```
###### Clear/Migrate postrgesql table
```
> docker-compose exec web python manage.py create_db
```

###### After these commands job is automatically running,
###### Starting data is populated, and every 5 minutes new data is inserted


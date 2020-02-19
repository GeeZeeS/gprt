# gprt
docker-compose build

sudo docker-compose up -d

docker-compose exec web python manage.py seed_db

sudo docker-compose exec db psql --username=user --dbname=pg_db
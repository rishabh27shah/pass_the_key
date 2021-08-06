# Instructions

Django application to help franchise acquisition team understand the value of
postcode districts in Greater Manchester.


## Commands to Run Project


```bash
cd pass_the_key
```

### Update values in .env file in project root directory

```bash
sudo docker-compose build
sudo docker-compose up -d
sudo docker-compose exec web python manage.py migrate --settings=pass_the_key.settings.production
```

## Load resource data into database

```bash
sudo docker-compose exec web python manage.py setupdb --settings=pass_the_key.settings.production
```

## Testing

```bash
sudo docker-compose exec web python manage.py test --settings=pass_the_key.settings.production
```

## Swagger

You can checkout swagger at /api/swagger
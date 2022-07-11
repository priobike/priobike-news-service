# News Service
A microservice to create and publish news to the PrioBike app.

## REST-API Endpoints
- ```api/news```: Get all news articles
    - optional query params:
        - ```last_sync_date```: Specifies the date (+ 1 day) from which on new news articles shoud be returned.
        - ```hash```: MD5-hash of all news articles (MD5-hash of json array of news articles) that got released on or before the ```last_sync_date```.
- ```api/category/<category_id>```: Get category for specific category id

## Schemes
- News article:
``` 
{
    "id": 2,
    "article_text": "...",
    "article_title": "...",
    "pub_date": "2022-07-11",
    "category_id": 3
}
```
- Category:
```
{
    "id": 1,
    "title": "..."
}
```

## Development
- Start local development server: ```poetry run python manage.py runserver```
- Run tests: ```poetry run python manage.py test```
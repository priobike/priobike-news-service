# priobike-news-service

A Django service that can be used to create/distribute news articles and send out push notifications.

This service is used in our app to keep users engaged with the PrioBike app after leaving for a longer time, notifying them of recent updates that may be worth to check out.

[Learn more about PrioBike](https://github.com/priobike)

## Quickstart

The easiest way to spin up a minimalistic setup with this service is to use the contained `docker-compose.yml`:

```
docker-compose up
```

## API

- ```api/news```: Get all news articles
    - optional query params:
        - ```from```: Specifies the date(time) from which on new news articles shoud be returned.released on or before the ```from``` date(time).
            - date(time) can be provided in the following formats:
                - ```2022-07-13``` (equivalent to ```2022-07-13T00:00:00.000000Z```)
                - ```2022-07-17T09:49:29Z``` (equivalent to ```2022-07-13T09:49:29.000000Z```)
                - ```2022-07-13T09:49:29.235744Z```
- ```api/category/<category_id>```: Get category for specific category id

## Examples
- Query: ```/news/articles?from=2022-07-17T08:14:41Z```
    - Response:
        ```
        [
            {
                "id": 2,
                "text": "Test-Text-2",
                "title": "Test-Title-2",
                "pub_date": "2022-07-17T09:49:29Z",
                "category_id": 1,
                "md5": "..."
            }
        ]
        ```
- Query: ```/news/articles?from=2022-07-16```
    - Response:
        ```
        [
            {
                "id": 2,
                "text": "Test-Text-2",
                "title": "Test-Title-2",
                "pub_date": "2022-07-17T09:49:29Z",
                "category_id": 1,
                "md5": "44539ce683b6a7b8509bfdc2916a3214"
            },
            {
                "id": 1,
                "text": "Test-Text-1",
                "title": "Test-Title-1",
                "pub_date": "2022-07-17T08:14:41Z",
                "category_id": 1,
                "md5": "..."
            }
        ]
        ```
- Query: ```/news/articles```
    - Response:
        ```
        [
            {
                "id": 2,
                "text": "Test-Text-2",
                "title": "Test-Title-2",
                "pub_date": "2022-07-17T09:49:29Z",
                "category_id": 1,
                "md5": "44539ce683b6a7b8509bfdc2916a3214"
            },
            {
                "id": 1,
                "text": "Test-Text-1",
                "title": "Test-Title-1",
                "pub_date": "2022-07-17T08:14:41Z",
                "category_id": 1,
                "md5": "..."
            }
        ]
        ```
- Query: ```/news/category/1```
    - Response:
        ```
        {
            "id": 1,
            "title": "Test"
        }
        ```

## CLI

- Create local SQLLite database:  ```poetry run python manage.py migrate```
- Create super user for Django admin panel: ```poetry run python manage.py createsuperuser```
- Start local development server: ```poetry run python manage.py runserver```
- Run tests: ```poetry run python manage.py test```

## What else to know

This service can be executed in two modes: **manager** and **worker** mode. The **worker** mode is made to hit requests from users and can be scaled horizontally. The **manager** mode is designed to be deployed once, coordinating the workers. In the news service, the manager is used to create news articles via the Django admin interface. After an article is created, the content of this article is sent to all workers in the docker network, from where clients can fetch the detailled contents of each news article.

## Contributing

We highly encourage you to open an issue or a pull request. You can also use our repository freely with the `MIT` license. 

Every service runs through testing before it is deployed in our release setup. Read more in our [PrioBike deployment readme](https://github.com/priobike/.github/blob/main/wiki/deployment.md) to understand how specific branches/tags are deployed.

## Anything unclear?

Help us improve this documentation. If you have any problems or unclarities, feel free to open an issue.

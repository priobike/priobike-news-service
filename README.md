# News Service
A microservice to create and publish news to the PrioBike app.

## WORKER REST-API Endpoints
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

## Development
- Create local SQLLite database:  ```poetry run python manage.py migrate```
- Create super user for Django admin panel: ```poetry run python manage.py createsuperuser```
- Start local development server: ```poetry run python manage.py runserver```
- Run tests: ```poetry run python manage.py test```
 

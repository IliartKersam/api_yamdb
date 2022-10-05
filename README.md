# Yamdb API

### Yamdb - reviews resource

##### Description


The YaMDb project collects reviews (Review) of users on works (Titles). The works are divided into categories: "Books", "Films", "Music". The list of categories (Category) can be expanded by the administrator (for example, you can add the category "Fine Arts" or "Jewellery").

##### Technologies

- Python 3.7
- Django 2.2.19
- Django REST framework

### How to run the project:

Clone repository and go to it's derictory on your computer:
```
git clone https://github.com/IliartKersam/api_yamdb.git
```
```
cd api_yamdb
```

Create and activate virtual environment:

```
python -m venv venv
```
```
source venv/bin/activate
```
```
python -m pip install --upgrade pip
```

Install the requirements from requirements.txt:
```
pip install -r requirements.txt
```

Migrate:
```
python manage.py migrate
```

Run the project:
```
python manage.py runserver
```

### Available endpoints

#### Registration

Sign up:

`api/v1/auth/signup/`

Getting a token:

`api/v1/auth/token/`

#### Categories

All categories:

`api/v1/categories/`

#### Genres

All genres:

`api/v1/genres/`

#### Titles

All titles:

`api/v1/titles/`

Title's details:

`api/v1/titles/{title_id}/`

#### Reviews

All reviews:

`api/v1/titles/{title_id}/reviews/`

Reviews' details:

`api/v1/titles/{title_id}/reviews/{review_id}/`

#### Comments

All reviews' comments:

`api/v1/titles/{title_id}/reviews/{review_id}/comments/`

Comment details:

`api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/`

#### Users

All users:

`api/v1/users/`

User's details:

`api/v1/users/{username}/`

Your details:

`api/v1/users/me/`


### Authors

1. Auth/Users - Kseniya Nivnya
2. Categories/Genres/Titles - Elina Anastasia
3. Review/Comments - Kashtanov Nikolai

Moscow, 2022

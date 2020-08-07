# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup

Before flushing the data into the database, we need to create the database named 'trivia' via:
```bash
createdb trivia
```
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
This will flush the data into the trivia database.
## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## Endpoints Reference

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
- METHOD URL: ``` curl http://127.0.0.1:5000/categories ```
- Sample: 
```bash
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true,
    "total_category": 6
}

```

GET '/questions'
- Fetches a list of questions that contains in the database
- The list includes 'answer', 'category', 'difficulty', 'id', and 'question' itself.
- Return an object that inclues categories, current_categories, questions, status, total_questions.
- METHOD URL: ``` curl http://127.0.0.1:5000/questions ```
- Sample:
```bash
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_categories": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    }
  ],
  "success": true,
  "total_question": 32
}
```

DELETE '/questions/<int:question_id>'
- Delete question by providing question id
- reutrn status of delete and deleted question id
- METHOD URL: ``` curl http://127.0.0.1:5000/questions/13 -X DELETE ```
- Sample:
```bash
{
    'deleted': 13,
    'success': True
}
```

POST '/questions'
- Post method to post new question to the database
- Arguments: question, answer, category, difficulty.
- METHOD URL: ``` curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "Who is the first asian american nba player won the champion?", "answer": "Jeremy Lin", "difficulty": 2, "category": "6" }'  ```
- Sample:
```bash
{
  "created": 42,
  "questions": [
    {
      "answer": "Jeremy Lin",
      "category": 6,
      "difficulty": 2,
      "id": 42,
      "question": "Who is the first asian american nba player won the champion?"
    }
  ],
  "success": true,
  "total_questions": 32
}
```

POST '/questions/search'
- Post a search string in the questions.
- Return any questions for whom search term is a substring of the question
- METHOD URL: ``` curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "who"}' ```
- Sample:
```bash
{
  "questions": [
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Jeremy Lin",
      "category": 6,
      "difficulty": 2,
      "id": 42,
      "question": "Who is the first asian american nba player won the champion?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

GET '/categories/<int:category_id>/questions'
- Get questions from specific category
- METHOD URL: ``` curl http://127.0.0.1:5000/categories/6/questions ```
- Sample:
``` bash
{
  "category": 6,
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "Jeremy Lin",
      "category": 6,
      "difficulty": 2,
      "id": 42,
      "question": "Who is the first asian american nba player won the champion?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

POST '/quizzes'
- Post randomly from categories.
- Able to select all the categories or a specific one.
- The questions from the category will jump up randomly but without previous shown ones.
- METHOD URL: ``` curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [42], "quiz_category": {"type": "Sports", "id": "6"}}' ```
- Sample:
``` bash
{
  "question": {
    "answer": "Brazil",
    "category": 6,
    "difficulty": 3,
    "id": 10,
    "question": "Which is the only team to play in every soccer World Cup tournament?"
  },
  "success": true
}
```

## Error handling

The error will be return as JSON format as followed:
Not found error (404)
```bash
{
"error": 404,
"message": "not found",
"success": false
}
```
Unprocessable error (422)
```bash
{
"error": 422,
"message": "unprocessable entity",
"success": false
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py
```

## Authors
Jeffrey Lee is in charged of backend Web Api in (__init__.py) and (test_flask.py) files. Also the README in the backend.
All other files are contributed by Udacity- Full Stack Web Developer Nanodegree.
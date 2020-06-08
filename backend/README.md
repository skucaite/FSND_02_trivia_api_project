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
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

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

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

**************************************
**************************************
*********** REVIEW_COMMENT ***********
**************************************
**************************************

```GETTING STRATED```
  - Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, with is set as a proxy in the frontend configuration.
  - Authentication: This version of the application does not require authentication or API keys.


```ERROR HANDLING```
  - Errors are returned as JSON objects in the following format:

    {
      "success": False,
      "error": 400,
      "message": "bad request"
    }

    The API will return three error types when requests fail:
      * 400: Bad request
      * 404: Resource Not found
      * 405: Method not allowed
      * 422: Not Processable


```ENDPOINTS```
  - GET /categories
    * General:
      - Returns a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category (id: category_string) and success value.
    * Sample: curl http://127.0.0.1:5000/categories
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}


  - GET /questions
    * General:
      - Returns a list of questions, number of total questions, current category (which is None), categories and success value.
     - Questions are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
    * Sample: curl http://127.0.0.1:5000/questions
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
   #  .... shows all 10 questions per page .....  #
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }

  ],
  "success": true,
  "totalQuestions": 19
}


  - DELETE /questions/{question_id}
    * General:
        - Deletes the question of the given ID if exist. Returns the id of the deleted question, success value, total questions and question list based on current page number to update the frontend.
    * Sample: curl -X DELETE http://127.0.0.1:5000/questions/5
  "deleted": 5,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": "5",
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
   #  .... shows all 10 questions per page .....  #
    {
      "answer": "Agra",
      "category": "3",
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 18
}


  - POST /questions
    * General:
        - Creates a new question using the submitted question text, answer text, category and difficulty score. Returns the id of the created question, success value, total books and question list based on current page number to update the frontend.
    * Sample: curl http://127.0.0.1:5000/questions?page=2 -X POST -H "Content-Type: application/json" -d '{"question": "Whose autobiography is entitled \'I Know Why the Caged Bird Sings\'?", "answer": "Maya Angelou", "category": "4", "difficulty": "2"}'

  "created": 25,
  "questions": [
    {
      "answer": "Escher",
      "category": "2",
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
   #  .... shows all 10 questions per page .....  #
    {
      "answer": "Maya Angelou",
      "category": "4",
      "difficulty": 2,
      "id": 25,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }

  ],
  "success": true,
  "total_questions": 19
}


  - GET /categories/{category_id}/questions
    * General:
      - Returns a list of questions, number of total questions, current category type and success value.
     - Questions are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
    * Sample: curl http://127.0.0.1:5000/categories/3/questions

  "current_category": "Geography",
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": "3",
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": "3",
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": "3",
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "totalQuestions": 3
}





## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

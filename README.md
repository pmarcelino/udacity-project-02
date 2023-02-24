# API Development and Documentation Final Project

## Trivia App

This app is a full-stack web application that allows users to view, manage, and play trivia questions. It provides a user-friendly interface that allows users to interact with the app seamlessly.

The app features a variety of functionalities, including the ability to display all questions and questions by category, delete questions, add questions, and search for questions based on a text query string. Additionally, users can play a quiz game, either randomizing all questions or within a specific category.

The app is built using modern web technologies, including Python, Flask, SQLAlchemy, and JavaScript. It is designed to be flexible, scalable, and maintainable, making it ideal for use in a wide range of web development projects.

In this README file, you'll find detailed information on how to set up, configure, and use the app. Additionally, we've included information on how to run tests and troubleshoot any issues that may arise.

We hope you enjoy using the Trivia App.

## Pre-requisites and Local Development 

Developers using this project should already have Python3, pip and node installed on their local machines.

### Backend

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands: 
```
export FLASK_APP=flaskr
export FLASK_DEBUG=1
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in debug mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application will run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration.

> View the [Backend README](./backend/README.md) for more details.

### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

The frontend will run on `http://127.0.0.1:3000/` by default.

> View the [Frontend README](./frontend/README.md) for more details.

## Tests

In order to run tests navigate to the `backend` folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the `dropdb` command. 

All tests are kept in that file and should be maintained as updates are made to app functionality.
## API reference
### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Endpoints 
#### GET /categories

- This endpoint retrieves a list of all available categories.
- Response:
  - categories: A dictionary of categories, with the ID as the key and the type of category as the value.
  - success: True if the request was successful, False otherwise.
  - total_categories: The total number of available categories.
- Sample: `curl http://127.0.0.1:5000/categories`

``` 
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
  "total_categories": 6
}
```

#### GET /questions?page=${page}

- This endpoint gets all questions from the database and paginates them. A default of 10 questions per page is considered.
- Requested arguments:
  - page: Integer that represents the page number.
- Response:
  - categories: A dictionary of categories, with the ID as the key and the type of category as the value.
  - current_category: The ID of the current category.
  - questions: A list of questions for the current page.
  - success: True if the request was successful, False otherwise.
  - total_questions: The total number of available questions.
  
- Sample: `curl http://127.0.0.1:5000/questions?page=1`

``` 
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
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```
#### DELETE /questions/<<int:question_id>>

- This endpoint deletes a question identified by its ID.
- Requested arguments:
  - question_id: The ID of the question to delete.
- Response:
  - deleted_question: The ID of the deleted question.
  - success: True if the request was successful, False otherwise.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/2`

``` 
{
  "deleted_question": 2,
  "success": true
}
```
#### POST /questions

- This endpoint handles post requests for questions.
- A new question will be posted unless the request includes a search term.

##### New question
- Request body:
  - question: The question text.
  - answer: The answer text.
  - difficulty: The difficulty of the question.
  - category: The category of the question.
- Response:
  - answer: The answer text.
  - category: The category of the question.
  - difficulty: The difficulty of the question.
  - question: The question text.
  - success: True if the request was successful, False otherwise.
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is the biggest football club in Portugal?","answer":"Benfica","difficulty":1,"category":"6"}'`
```
{
  "answer": "Benfica",
  "category": "6",
  "difficulty": 1,
  "question": "What is the biggest football club in Portugal?",
  "success": true
}
```

##### Search term
- Request body:
  - searchTerm: The search term.
- Response:
  - current_category: The ID of the current category.
  - questions: The list of questions that include the search term.
  - success: True if the request was successful, False otherwise.
  - total_questions: The total number of questions that include the search term.
- Sample: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'`
```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```
#### GET /categories/<<int:category>>/questions

- This endpoint gets questions in a specific category.
- Requested arguments:
  - category: The ID of the category in relation to which we want the questions.
- Response:
  - current_category: The ID of the current category.
  - questions: A list of questions in the specified category.
  - success: True if the request was successful, False otherwise.
  - total_questions: The total number of questions in the specified category.
  
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`

``` 
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```
#### POST /quizzes

- This endpoint plays the quiz.
- Request body:
  - previous_questions: A list of IDs of questions that have already been answered.
  - quiz_category: The category of the quiz.
- Response:
  - success: True if the request was successful, False otherwise.
  - question: A randomly selected question for the quiz or None if there are no further questions.
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[],"quiz_category":{"type":"History","id":"4"}}'`

```
{
  "question": {
    "answer": "Muhammad Ali",
    "category": 4,
    "difficulty": 1,
    "id": 9,
    "question": "What boxer's original name is Cassius Clay?"
  },
  "success": true
}
```
### Error Handling

The Trivia App also includes error handling for the following HTTP status codes:
- 404: Resource Not Found
- 422: Not Processable 
- 500: Internal Server Error

Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "resource not found"
}
```

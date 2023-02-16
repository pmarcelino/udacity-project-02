import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
SEED = 42

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    

    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_object('config')
    
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def retrieve_categories():
        # categories = list(set([category.type for category in Category.query.all()]))
        categories = Category.query.all()
        categories_dict = {}
        for category in categories:
            category_data = category.format()
            categories_dict[category_data["id"]] = category_data["type"]
            
        
        if categories == []:
            print(sys.exc_info())
            abort(404)
        
        return jsonify({"success":True, 
                        "categories":categories_dict, 
                        "total_categories":len(categories)})

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def get_questions():
        try:
            questions = Question.query.all()
            current_questions = paginate_questions(request, questions)
            
            categories = Category.query.all()
            categories_dict = {}
            for category in categories:
                category_data = category.format()
                categories_dict[category_data["id"]] = category_data["type"]
            
            return jsonify({"success": True,
                            "questions": current_questions,
                            "total_questions": len(questions),
                            "current_category": None,  # TODO: not sure about this
                            "categories": categories_dict
                            })
            
        except:
            abort(422)
            

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        
        if question is None:
            abort(404)
            
        try:
            question.delete()
            
            return jsonify({"success": True,
                        "deleted_question": question_id})
            
        except:
            print(sys.exc_info())
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def handle_questions_post():
        body = request.get_json()
        search_term = body.get("searchTerm", None)  # TODO: fix case when searchTerm is None but we are trying to do a search and not a post
        
        if search_term:
            return search_questions(search_term)
        else:
            return post_question()
        
    def post_question():
        try:
            body = request.get_json()
            question = body.get("question", None)
            answer = body.get("answer", None)
            category = body.get("category", None)
            difficulty = body.get("difficulty", None)
            
            question_obj = Question(question, answer, category, difficulty)
            question_obj.insert()
            
            return jsonify({"success": True,
                        "question": question,
                        "answer": answer,
                        "category": category,
                        "difficulty": difficulty})
            
        except:
            print(sys.exc_info())
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    def search_questions(search_term):
        questions = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
        questions = [question.format() for question in questions]
        
        return jsonify({"success": True,
                        "questions": questions,
                        "total_questions": len(questions),
                        "current_category": None})

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category>/questions")
    def get_category_questions(category):
        try:
            questions = Question.query.filter_by(category = category).all()
            questions = [question.format() for question in questions]
            
            return jsonify({"success": True,
                        "questions": questions,
                        "total_questions": len(questions),
                        "current_category": category
                        })
            
        except:
            print(sys.exc_info())
            abort(422)
        
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def quiz():  # TODO: do I want this structure? or should I put everything inside the try?
        try:
            body = request.get_json()
            previous_questions = body.get("previous_questions", None)
            quiz_category= body.get("quiz_category", None)
            
            # categories = list(set([category.id for category in Category.query.all()]))
            # if quiz_category not in categories:
            #     abort(404)
            
            questions = Question.query.filter(Question.categories.has(type=quiz_category["type"])).all()
            questions = [question.format() for question in questions]
            possible_questions = [question for question in questions if question["id"] not in previous_questions]
            
            # if possible_questions == []:
            #     abort(422)
            
            question = random.choice(possible_questions)
            
            return jsonify({"success": True,
                            "question": question})
        
        except:
            print(sys.exc_info())
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}), 404
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422
        )

    return app



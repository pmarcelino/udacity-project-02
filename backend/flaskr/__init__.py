import random
import sys

from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10
SEED = 42

def paginate_questions(request, selection):
    """Get a list of questions based on the given page number.
    
    Args:
        request (object): The request object
        selection (list): List of questions
    
    Returns:
        current_questions (list): Current page's questions
        
    """
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def build_categories_dict():
    """Returns a dictionary of categories, with the ID as the key and the type of category as the value.

    Args:
        None

    Returns:
        categories_dict (dict): dictionary of categories, with the ID as the key and the type of category as the value

    """
    categories = Category.query.all()
    categories_dict = {}
    for category in categories:
        category_data = category.format()
        categories_dict[category_data["id"]] = category_data["type"]
        
    return categories_dict
            

def create_app(test_config=None):
    """Create Flask app.

    Args:
        test_config (dict): Development environment configurations.

    Returns:
        app (Flask): Flask app.

    """
    app = Flask(__name__)
    
    if test_config:
        app.config.from_mapping(test_config)
    else:
        app.config.from_object('config')
    
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/categories")
    def get_categories():
        """Retrieves a list of all available categories"""
        try:
            categories_dict = build_categories_dict()    
            
            if len(categories_dict) == 0:
                print(sys.exc_info())
                abort(404)
            
            return jsonify({"success":True, 
                            "categories":categories_dict, 
                            "total_categories":len(categories_dict)})
        except:
            print(sys.exc_info())
            abort(422)

    @app.route("/questions")
    def get_questions():
        """Gets all questions from the database and paginates them"""
        try:
            questions = Question.query.all()
            
            if len(questions) == 0:
                print(sys.exc_info())
                abort(404)
            
            current_questions = paginate_questions(request, questions)
            categories_dict = build_categories_dict()
            
            return jsonify({"success": True,
                            "questions": current_questions,
                            "total_questions": len(questions),
                            "current_category": None,
                            "categories": categories_dict
                            })
        except:
            print(sys.exc_info())
            abort(422)

    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        """Deletes a question identified by its ID"""
        try:
            question = Question.query.get(question_id)
        
            if question is None:
                print(sys.exc_info())
                abort(404)
                
            question.delete()
            
            return jsonify({"success": True,
                        "deleted_question": question_id})
        except:
            print(sys.exc_info())
            abort(422)

    @app.route("/questions", methods=["POST"])
    def handle_questions_post():
        """Handles post requests for questions.
       
        If the request includes a search term, the corresponding questions will be searched. If not, a new question will be posted.
        
        """
        body = request.get_json()
        search_term = body.get("searchTerm", None)
        question = body.get("question", None)
        
        if search_term:
            return search_questions(search_term)
        elif question:
            return post_question(question)
        else:
            print(sys.exc_info())
            abort(404)
        
    def post_question(question):
        """Handles the requests to post a new question"""
        try:
            body = request.get_json()
            answer = body.get("answer", None)
            category = body.get("category", None)
            difficulty = body.get("difficulty", None)
            
            if "" in (question, answer):
                print(sys.exc_info())
                abort(404)
            
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

    def search_questions(search_term):
        """Search for questions in the current database"""
        try:
            questions = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
            questions = [question.format() for question in questions]
            
            return jsonify({"success": True,
                            "questions": questions,
                            "total_questions": len(questions),
                            "current_category": None})
        except:
            print(sys.exc_info())
            abort(422)

    @app.route("/categories/<int:category>/questions")
    def get_category_questions(category):
        """Gets questions in a specific category"""
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
        
    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        """Play the quiz"""
        try:
            body = request.get_json()
            previous_questions = body.get("previous_questions", None)
            quiz_category= body.get("quiz_category", None)
            
            if quiz_category["id"] != 0:
                questions = Question.query.filter(Question.categories.has(type=quiz_category["type"])).all()
            else:
                questions = Question.query.all()
                
            questions = [question.format() for question in questions]
            possible_questions = [question for question in questions if question["id"] not in previous_questions]
            
            if len(possible_questions) == 0:
                print(sys.exc_info())
                abort(404)
                
            question = random.choice(possible_questions)
            
            return jsonify({"success": True,
                            "question": question})
        
        except:
            print(sys.exc_info())
            abort(422)

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



import random
import sys

from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Question, Category, db

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
        categories_dict (dict): Dictionary of categories, with the ID as the key and the type of category as the value

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
        categories_dict = build_categories_dict()  
        
        if len(categories_dict) == 0:
            # print(sys.exc_info())
            abort(404)
        
        return jsonify({"success": True, 
                        "categories": categories_dict, 
                        "total_categories": len(categories_dict)})
        
    @app.route("/questions")
    def get_questions():
        """Gets all questions from the database and paginates them"""
        questions = Question.query.all()
        
        current_questions = paginate_questions(request, questions)
        
        if current_questions == []:
            # print(sys.exc_info())
            abort(404)
        
        categories_dict = build_categories_dict()
        
        return jsonify({"success": True,
                        "questions": current_questions,
                        "total_questions": len(questions),
                        "current_category": None,
                        "categories": categories_dict
                        })
        
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        """Deletes a question identified by its ID"""
        question = Question.query.filter_by(id=question_id).one_or_none()
        
        if question is None:
            # print(sys.exc_info())
            abort(404)
        
        try:
            question.delete()
        except:
            # print(sys.exc_info())
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()
        
        return jsonify({"success": True,
                        "deleted_question": question_id})

    @app.route("/questions", methods=["POST"])
    def handle_questions_post():
        """Handles post requests for questions.
       
        If the request includes a search term, the corresponding questions will be searched. If not, a new question will be posted.
        
        """
        body = request.get_json()
        
        question = body.get("question", None)
        if question is not None:
            return post_question(body, question)
        
        search_term = body.get("searchTerm", None)
        return search_questions(search_term)  # If searchTerm==None, returns all questions
        
    def post_question(body, question):
        """Handles the requests to post a new question"""
        answer = body.get("answer", None)
        category = body.get("category", None)
        difficulty = body.get("difficulty", None)
        
        if "" in (question, answer):
            # print(sys.exc_info())
            abort(422)
        
        try:
            question_obj = Question(question, answer, category, difficulty)
            question_obj.insert()
            
        except:
            # print(sys.exc_info())
            db.session.rollback()
            abort(500)
        finally:
            db.session.close()
        
        return jsonify({"success": True,
                        "question": question,
                        "answer": answer,
                        "category": category,
                        "difficulty": difficulty})
            

    def search_questions(search_term):
        """Search for questions in the current database"""
        questions = Question.query.filter(Question.question.ilike(f"%{search_term}%")).all()
        questions = [question.format() for question in questions]
        
        return jsonify({"success": True,
                        "questions": questions,
                        "total_questions": len(questions),
                        "current_category": None})
        
    @app.route("/categories/<int:category>/questions")
    def get_category_questions(category):
        """Gets questions in a specific category"""
        questions = Question.query.filter_by(category = category).all()
        questions = [question.format() for question in questions]
        
        return jsonify({"success": True,
                        "questions": questions,
                        "total_questions": len(questions),
                        "current_category": category
                        })
        
    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        """Play the quiz"""
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
            # print(sys.exc_info())
            abort(404)
            
        question = random.choice(possible_questions)
        
        return jsonify({"success": True,
                        "question": question})
    
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
        
    @app.errorhandler(500)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 500, "message": "internal server error"}), 500
        )

    return app



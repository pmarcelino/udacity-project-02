import os
import subprocess
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app"""
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        test_config = {
            'SQLALCHEMY_DATABASE_URI': self.database_path,
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
            }
        
        self.app = create_app(test_config)
        self.client = self.app.test_client
        
        self.message_404 = "resource not found"
        self.message_422 = "unprocessable"
        
    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_categories(self):
        """Test it gets available categories"""
        # Given
        status_code = 200
        categories = {
            "1": "Science",
            "2": "Art",
            "3": "Geography",
            "4": "History",
            "5": "Entertainment",
            "6": "Sports"
        }
        total_categories = 6
        
        # When
        res = self.client().get("/categories")
        data = json.loads(res.data)
        
        # Then
        self.assertEqual(res.status_code, status_code)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["categories"], categories)
        self.assertEqual(data["total_categories"], total_categories)
    
    def test_get_questions(self):
        """Test it gets the questions"""
        # Given
        status_code = 200
        
        # When
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        # Then
        self.assertEqual(res.status_code, status_code)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        
    def test_404_get_questions_invalid_page(self):
        """Test get question fails when an invalid page is given"""
        # Given
        page = 999999999
        status_code = 404
        message = self.message_404
        
        # When
        res = self.client().get(f"/questions?page={page}")
        data = json.loads(res.data)
        
        # Then
        self.assertEqual(res.status_code, status_code)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], message)
    
    # def test_delete_question(self):
    #     """Test delete question"""
    #     # Given
    #     res = self.client().get("/questions")
    #     data = json.loads(res.data)
    #     question_id = data["questions"][-1]["id"]  # Get the last question in the database
        
    #     status_code = 200
        
    #     # When
    #     res = self.client().delete(f"/questions/{question_id}")
    #     data = json.loads(res.data)
        
    #     # Then
    #     self.assertEqual(res.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertEqual(data["deleted_question"], question_id)
    
    def test_404_delete_question_invalid_id(self):
        """Test delete question fails the question id is invalid"""
        # Given
        question_id = 999999999
        status_code = 404
        message = self.message_404
        
        # When
        res = self.client().delete(f"/questions/{question_id}")
        data = json.loads(res.data)
        
        # Then
        self.assertEqual(res.status_code, status_code)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], message)
        
    def test_post_question(self):
        """Test post question"""
        # Given
        question = "Test question"
        answer = "Test answer"
        category = 2
        difficulty = 1
        
        data = {"question": question,
                "answer": answer,
                "category": category,
                "difficulty": difficulty}
        
        status_code = 200
        
        # When
        res = self.client().post("/questions", json = data)
        data = json.loads(res.data)
        
        # Then
        self.assertEqual(res.status_code, status_code)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["question"], question)
        self.assertEqual(data["answer"], answer)
        self.assertEqual(data["category"], category)
        self.assertEqual(data["difficulty"], difficulty)
        
    def test_422_post_question_fails_missing_question(self):
        """Test post question fails when the question is missing"""
        # Given
        question = ""
        answer = "Test answer"
        category = 2
        difficulty = 1
        
        data = {"question": question,
                "answer": answer,
                "category": category,
                "difficulty": difficulty}
        
        status_code = 422
        message = self.message_422
        
        # When
        res = self.client().post("/questions", json = data)
        data = json.loads(res.data)
        
        # Then
        self.assertEqual(res.status_code, status_code)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], message)
    
    def test_422_post_question_fails_missing_answer(self):
        """Test post question fails when the answer is missing"""
        # Given
        question = "Test question"
        answer = ""
        category = 2
        difficulty = 1
        
        data = {"question": question,
                "answer": answer,
                "category": category,
                "difficulty": difficulty}
        
        status_code = 422
        message = self.message_422
        
        # When
        res = self.client().post("/questions", json = data)
        data = json.loads(res.data)
        
        # Then
        self.assertEqual(res.status_code, status_code)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], message)
    
    def test_search_questions(self):
        """Test it can search questions given a search term"""
        # Given
        search_term = "title"
        query_data = {"searchTerm": search_term}
        
        total_questions = 2
        questions = [
            {
                'id': 5, 
                'question': "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?", 
                'answer': 'Maya Angelou', 
                'category': 4, 
                'difficulty': 2
            }, 
            {
                'id': 6, 
                'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?', 
                'answer': 'Edward Scissorhands', 
                'category': 5, 
                'difficulty': 3
            }
        ]
        
        # When
        res = self.client().post("/questions", json=query_data)
        data = json.loads(res.data)
        
        # Then
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["questions"], questions)
        self.assertEqual(data["total_questions"], total_questions)
        
    def test_get_category_questions(self):
        """Test get category questions"""
        # Given
        category = 1
        status_code = 200
        
        first_question = {'id': 20, 
                          'question': 'What is the heaviest organ in the human body?', 
                          'answer': 'The Liver', 
                          'category': 1, 
                          'difficulty': 4}
        total_questions = 3
        
        # When
        res = self.client().get(f"/categories/{category}/questions")
        data = json.loads(res.data)
        
        # Then
        self.assertEqual(res.status_code, status_code)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["questions"][0], first_question)
        self.assertEqual(data["total_questions"], total_questions)
    
    def test_quiz_all_categories(self):
        """Test quiz works for all categories"""
        # Given
        previous_questions = []
        quiz_category = {"id": 0, "type": "click"}
        
        data = {
            "previous_questions": previous_questions,
            "quiz_category": quiz_category
        }
        
        # When
        res = self.client().post("/quizzes", json=data)
        data = json.loads(res.data)
        
        # Then
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_quiz_specific_category(self):
        """Test quiz works for a specific category"""
        # Given
        previous_questions = [5, 12]
        quiz_category = {"id": 4, "type": "History"}
        possible_questions = [
            {
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1,
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?"
            },
            {
                "answer": "Scarab",
                "category": 4,
                "difficulty": 4,
                "id": 23,
                "question": "Which dung beetle was worshipped by the ancient Egyptians?"
            }
        ]
        
        data = {"previous_questions": previous_questions,
                "quiz_category": quiz_category}
        
        # When
        res = self.client().post("/quizzes", json = data)
        data = json.loads(res.data)
        
        # Then
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"] in possible_questions)
        
    def test_404_quiz_no_questions(self):
        """Test quiz fails when no questions are available"""
        # Given
        previous_questions = []
        quiz_category = {"id": 999999999, "type": "Dragon Ball"}  # Invalid category will raise no questions scenario
        
        data = {
            "previous_questions": previous_questions,
            "quiz_category": quiz_category
        }
        
        status_code = 404
        message = self.message_404
        
        # When
        res = self.client().post("/quizzes", json=data)
        data = json.loads(res.data)
        
        # Then
        self.assertEqual(res.status_code, status_code)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], message)
    
if __name__ == "__main__":
    unittest.main()
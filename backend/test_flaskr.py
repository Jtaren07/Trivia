import os
import unittest
import json


from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', 'eazye5000', 'localhost:5432', self.database_name)
        self.app = create_app({
            'database_path': self.database_path
        })
        self.client = self.app.test_client
        # Bind the app to the current context
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Executed after reach test"""
        # db.session.remove()
        self.app_context.pop()

    """
    TODO
    Write at least one test for each endpoint in __init__.py.
    Test for successful operation and for expected errors.
    """    
    def test_get_categories_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_paginated_questions_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

   
    
    def test_delete_question_success(self):
        """Test successful deletion of a question"""
        # Create a dummy question to delete
        question = Question(question='Test Question', answer='Test Answer', 
                            category=1, difficulty=1)
        question.insert()
        question_id = question.id

        res = self.client().delete(f'/questions/{question_id}')
        data = json.loads(res.data)

        question_check = Question.query.filter(Question.id == question_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question_id)
        self.assertEqual(question_check, None)
        

    def test_404_if_question_does_not_exist(self):
        """Test deleting a question that doesn't exist returns 404"""
        res = self.client().delete('/questions/999999')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_quiz_success(self):
        """Test successful quiz play"""
        quiz_round = {'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': 1}}
        response = self.client().post('/quizzes', json=quiz_round)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_422_quiz_failure(self):
        """Test quiz failure with missing data"""
        response = self.client().post('/quizzes', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
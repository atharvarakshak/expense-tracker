import unittest
import os
import tempfile
from app import create_app
from app.db import db, User, Statements
from app.functions import get_base64_encode
import datetime


class HomeRouteTestCase(unittest.TestCase):
    """Test cases for the home page route '/'"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary database file
        self.db_fd, self.db_path = tempfile.mkstemp()
        
        # Set up test configuration
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{self.db_path}'
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SECRET_KEY'] = 'test-secret-key'
        
        self.client = self.app.test_client()
        
        # Create application context and database tables
        with self.app.app_context():
            db.create_all()
            
            # Create a test user
            self.test_user = User(
                name='Test User',
                email='test@example.com',
                password='hashed_password',
                session_id='test_session_123'
            )
            db.session.add(self.test_user)
            db.session.commit()
            
            # Create some test statements
            self.test_statements = [
                Statements(
                    description='Test Income',
                    amount=1000.00,
                    operation_time=datetime.datetime.now(),
                    statement_id='stmt_001',
                    user_id=self.test_user.id
                ),
                Statements(
                    description='Test Expense',
                    amount=-500.00,
                    operation_time=datetime.datetime.now(),
                    statement_id='stmt_002',
                    user_id=self.test_user.id
                )
            ]
            
            for stmt in self.test_statements:
                db.session.add(stmt)
            db.session.commit()

    def tearDown(self):
        """Clean up after each test method."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_home_route_without_authentication(self):
        """Test that unauthenticated users are redirected to login"""
        response = self.client.get('/')
        
        # Should redirect to auth page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth', response.location)

    def test_home_route_with_authentication(self):
        """Test that authenticated users can access the home page"""
        # Set up session to simulate logged-in user
        with self.client.session_transaction() as sess:
            sess['session-sign-id'] = get_base64_encode('test_session_123')
        
        response = self.client.get('/')
        
        # Should return 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Check that the response contains expected content
        self.assertIn(b'Test User', response.data)

    def test_home_route_displays_user_data(self):
        """Test that the home page displays correct user data"""
        # Set up session to simulate logged-in user
        with self.client.session_transaction() as sess:
            sess['session-sign-id'] = get_base64_encode('test_session_123')
        
        response = self.client.get('/')
        
        # Should return 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Check that user name is displayed
        self.assertIn(b'Test User', response.data)
        
        # The response should contain the rendered template
        # We can't easily check for specific balance values in the HTML
        # without parsing it, but we can verify the response is successful

    def test_home_route_with_invalid_session(self):
        """Test that users with invalid session are redirected"""
        # Set up session with invalid session ID
        with self.client.session_transaction() as sess:
            sess['session-sign-id'] = get_base64_encode('invalid_session_id')
        
        response = self.client.get('/')
        
        # Should redirect to auth page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/auth', response.location)

    def test_home_route_template_rendering(self):
        """Test that the home route renders the correct template"""
        # Set up session to simulate logged-in user
        with self.client.session_transaction() as sess:
            sess['session-sign-id'] = get_base64_encode('test_session_123')
        
        with self.app.test_request_context():
            response = self.client.get('/')
            
            # Should return 200 OK
            self.assertEqual(response.status_code, 200)
            
            # Response should contain HTML content
            self.assertTrue(response.data)
            self.assertIn(b'html', response.data.lower())


if __name__ == '__main__':
    unittest.main()

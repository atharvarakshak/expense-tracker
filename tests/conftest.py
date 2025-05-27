"""
Test configuration and fixtures for the expense tracker application.
"""
import os
import tempfile
import pytest
from app import create_app
from app.db import db


def create_test_app():
    """Create and configure a test Flask application."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    
    # Store the database file descriptor and path for cleanup
    app.db_fd = db_fd
    app.db_path = db_path
    
    return app


def cleanup_test_app(app):
    """Clean up test application resources."""
    if hasattr(app, 'db_fd') and hasattr(app, 'db_path'):
        os.close(app.db_fd)
        os.unlink(app.db_path)

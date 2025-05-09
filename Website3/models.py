"""
Database Models Module

This module defines the SQLAlchemy database models for the school management system.
It includes models for User authentication and Timetable management.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy instance
db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    User model for authentication and role-based access control.
    
    Attributes:
        id: Unique identifier for the user
        name: Full name of the user
        email: Email address (unique) used for login
        password_hash: Securely hashed password
        role: User role ('admin', 'teacher', or 'student')
    """
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(50))  # 'admin', 'teacher', 'student'

    def set_password(self, password):
        """
        Set the password hash from a plaintext password.
        
        Args:
            password: The plaintext password to hash and store
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verify a plaintext password against the stored hash.
        
        Args:
            password: The plaintext password to check
            
        Returns:
            bool: True if the password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)


class Timetable(db.Model):
    """
    Timetable model for storing course schedules.
    
    Each entry represents a scheduled class with details about
    the course, day, time, and associated user (teacher or student).
    
    Attributes:
        id: Unique identifier for the timetable entry
        course_name: Name of the course
        day: Day of the week when the class is scheduled
        time: Time when the class is scheduled
        user_id: Foreign key linking to the associated user
        user: Relationship to the User model
    """
    
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100))
    day = db.Column(db.String(50))
    time = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='timetables')
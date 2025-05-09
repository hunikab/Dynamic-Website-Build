"""
School Management System Flask Application

This application provides a web interface for managing school timetables,
with different roles for administrators, teachers, and students.

The system enables user authentication, role-based access control,
and CRUD operations for users and timetables.
"""

from flask import (
    Flask, render_template, redirect, url_for, request, flash, session
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_user, logout_user, login_required, current_user
)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from config import Config
from models import db, User, Timetable

# -------------App Configuration-------------
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


# -------------Login Manager Setup----------
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login user loader function.
    
    Args:
        user_id: The user ID to load from the database
    
    Returns:
        User object if found, None otherwise
    """
    return User.query.get(int(user_id))


# -------------Form Classes----------------
class LoginForm(FlaskForm):
    """Form for user login."""
    
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class StudentRegistrationForm(FlaskForm):
    """Registration form for student users."""
    
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6)]
    )
    courses = SelectMultipleField('Courses', choices=[], coerce=int)
    submit = SubmitField('Register')


class AdminUserForm(FlaskForm):
    """Form for administrators to create or edit users."""
    
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')  # Only required for new users
    submit = SubmitField('Save')


class TimetableForm(FlaskForm):
    """Form for creating and editing timetable entries."""
    
    course_name = StringField('Course Name', validators=[DataRequired()])
    day = StringField('Day', validators=[DataRequired()])
    time = StringField('Time', validators=[DataRequired()])
    teacher = SelectMultipleField('Assigned Teacher(s)', coerce=int)
    submit = SubmitField('Save')


# -------------Public Routes---------------
@app.route('/')
def index():
    """
    Root route that redirects to login page.
    
    Returns:
        Redirect to login page
    """
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handle user login and redirect based on user role.
    
    Returns:
        Rendered login template or redirect to appropriate dashboard
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)

            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif user.role == 'teacher':
                return redirect(url_for('teacher_dashboard'))
            elif user.role == 'student':
                return redirect(url_for('student_dashboard'))
            else:
                flash('Unknown user role.')
                logout_user()
                return redirect(url_for('login'))

        flash('Invalid email or password.')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """
    Handle user logout.
    
    Returns:
        Redirect to login page
    """
    logout_user()
    return redirect(url_for('login'))


@app.route('/student/register', methods=['GET', 'POST'])
def register_student():
    """
    Handle student registration process.
    
    Returns:
        Rendered registration form or redirect to login page after success
    """
    form = StudentRegistrationForm()
    teachers = User.query.filter_by(role='teacher').all()
    form.courses.choices = [(t.id, f"{t.name}'s Class") for t in teachers]

    if form.validate_on_submit():
        student = User(name=form.name.data, email=form.email.data, role='student')
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()

        for teacher_id in form.courses.data:
            teacher_courses = Timetable.query.filter_by(user_id=teacher_id).all()
            for tc in teacher_courses:
                db.session.add(Timetable(
                    course_name=tc.course_name,
                    day=tc.day,
                    time=tc.time,
                    user_id=student.id
                ))
        db.session.commit()

        flash('Registration successful. You can now log in.')
        return redirect(url_for('login'))

    return render_template('register_student.html', form=form)


# -------------Role-Specific Dashboard Routes---------------
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """
    Admin dashboard showing all users and timetables.
    
    Returns:
        Rendered admin dashboard template or redirect if unauthorized
    """
    if current_user.role != 'admin':
        flash('Unauthorized access')
        return redirect(url_for('login'))

    teachers = User.query.filter_by(role='teacher').all()
    students = User.query.filter_by(role='student').all()
    timetables = Timetable.query.all()

    return render_template(
        'admin_dashboard.html',
        teachers=teachers,
        students=students,
        timetables=timetables
    )


@app.route('/teacher/dashboard')
@login_required
def teacher_dashboard():
    """
    Teacher dashboard showing their assigned timetables.
    
    Returns:
        Rendered dashboard template or redirect if unauthorized
    """
    if current_user.role != 'teacher':
        flash('Unauthorized access')
        return redirect(url_for('login'))
    timetable = Timetable.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', timetable=timetable)


@app.route('/student/dashboard')
@login_required
def student_dashboard():
    """
    Student dashboard showing their course timetables.
    
    Returns:
        Rendered dashboard template or redirect if unauthorized
    """
    if current_user.role != 'student':
        flash('Unauthorized access')
        return redirect(url_for('login'))
    timetable = Timetable.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', timetable=timetable)


# ---------------Admin User Management Routes-------------------------
@app.route('/admin/user/create/<role>', methods=['GET', 'POST'])
@login_required
def create_user(role):
    """
    Admin route to create new users.
    
    Args:
        role: The role of the user to create (teacher or student)
    
    Returns:
        Rendered user form or redirect to admin dashboard after creation
    """
    if current_user.role != 'admin':
        flash('Unauthorized access')
        return redirect(url_for('login'))

    if role not in ['teacher', 'student']:
        flash('Invalid role.')
        return redirect(url_for('admin_dashboard'))

    form = AdminUserForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, role=role)
        if form.password.data:
            user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"{role.title()} created successfully.")
        return redirect(url_for('admin_dashboard'))

    return render_template(
        'admin_user_form.html', form=form, action="Create", role=role
    )


@app.route('/admin/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    """
    Admin route to edit existing users.
    
    Args:
        user_id: ID of the user to edit
    
    Returns:
        Rendered user form or redirect to admin dashboard after update
    """
    if current_user.role != 'admin':
        flash('Unauthorized access')
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)
    form = AdminUserForm(obj=user)

    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash('User updated successfully.')
        return redirect(url_for('admin_dashboard'))

    return render_template(
        'admin_user_form.html', form=form, action="Edit", role=user.role
    )


@app.route('/admin/user/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    """
    Admin route to delete a user.
    
    Args:
        user_id: ID of the user to delete
    
    Returns:
        Redirect to admin dashboard after deletion
    """
    if current_user.role != 'admin':
        flash('Unauthorized access')
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)

    if user.role == 'admin':
        flash('Cannot delete an admin.')
        return redirect(url_for('admin_dashboard'))

    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.')
    return redirect(url_for('admin_dashboard'))


# --------------Admin Timetable Management Routes-------------------------
@app.route('/admin/timetable/create', methods=['GET', 'POST'])
@login_required
def create_timetable():
    """
    Admin route to create new timetable entries.
    
    Returns:
        Rendered timetable form or redirect to admin dashboard after creation
    """
    if current_user.role != 'admin':
        flash('Unauthorized access')
        return redirect(url_for('login'))

    form = TimetableForm()
    teachers = User.query.filter_by(role='teacher').all()
    form.teacher.choices = [(t.id, t.name) for t in teachers]

    if form.validate_on_submit():
        for teacher_id in form.teacher.data:
            new_entry = Timetable(
                course_name=form.course_name.data,
                day=form.day.data,
                time=form.time.data,
                user_id=teacher_id
            )
            db.session.add(new_entry)
        db.session.commit()
        flash('Timetable created successfully.')
        return redirect(url_for('admin_dashboard'))

    return render_template('timetable_form.html', form=form, action="Create")


@app.route('/admin/timetable/edit/<int:timetable_id>', methods=['GET', 'POST'])
@login_required
def edit_timetable(timetable_id):
    """
    Admin route to edit existing timetable entries.
    
    Args:
        timetable_id: ID of the timetable entry to edit
    
    Returns:
        Rendered timetable form or redirect to admin dashboard after update
    """
    if current_user.role != 'admin':
        flash('Unauthorized access')
        return redirect(url_for('login'))

    entry = Timetable.query.get_or_404(timetable_id)
    form = TimetableForm(obj=entry)
    form.teacher.choices = [(entry.user.id, entry.user.name)]

    if form.validate_on_submit():
        entry.course_name = form.course_name.data
        entry.day = form.day.data
        entry.time = form.time.data
        db.session.commit()
        flash('Timetable updated.')
        return redirect(url_for('admin_dashboard'))

    # ---------Pre-select teacher for UI clarity----------------
    form.teacher.data = [entry.user.id]
    return render_template('timetable_form.html', form=form, action="Edit")


@app.route('/admin/timetable/delete/<int:timetable_id>')
@login_required
def delete_timetable(timetable_id):
    """
    Admin route to delete a timetable entry.
    
    Args:
        timetable_id: ID of the timetable entry to delete
    
    Returns:
        Redirect to admin dashboard after deletion
    """
    if current_user.role != 'admin':
        flash('Unauthorized access')
        return redirect(url_for('login'))

    entry = Timetable.query.get_or_404(timetable_id)
    db.session.delete(entry)
    db.session.commit()
    flash('Timetable deleted.')
    return redirect(url_for('admin_dashboard'))


#-------------Initialization Route-------------------(Check the seed.py)
@app.route('/init')
def init_users():
    """
    Initialize the database with sample users and timetables.
    
    Returns:
        Confirmation message upon successful initialization
    """
    # Create admin
    if not User.query.filter_by(email="admin@admin.com").first():
        admin = User(name="Admin", email="admin@admin.com", role="admin")
        admin.set_password("adminpass")
        db.session.add(admin)

    # Create teacher
    if not User.query.filter_by(email="teacher@teacher.com").first():
        teacher = User(name="Mr. Smith", email="teacher@teacher.com", role="teacher")
        teacher.set_password("teachpass")
        db.session.add(teacher)

        # Add sample timetable
        db.session.add(Timetable(
            course_name="Math 101", day="Monday", time="10:00 AM", user=teacher
        ))

    db.session.commit()
    return "Admin and Teacher created!"


# ------------Application Entry Point---------
if __name__ == '__main__':
    """Application entry point for direct execution"""
    with app.app_context():
        db.create_all()
    app.run(debug=True)
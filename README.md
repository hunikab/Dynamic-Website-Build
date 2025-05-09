# 🧠 Flask Projects – Complete Setup Guide

This repository contains three Flask-based web applications:

1. 🏫 Timetable Manager – role-based dashboard for admin, teachers, and students
2. 🍽️ Restaurant Menu Manager – create, update, and order food items
3. 👥 Address Book – store and manage contact information

---

## 🚀 Getting Started

All projects follow the same structure. Here’s how to set up and run them in your local environment.

### ✅ Requirements

- Python 3.10+
- pip
- Virtualenv
- (Optional) PostgreSQL (for Timetable Manager)

---

## 🐍 1. Setting Up the Virtual Environment

Open a terminal and run:

```bash
# Step 1: Navigate into a project folder
cd /path/to/your/project

# Step 2: Create a virtual environment
python3 -m venv venv

# Step 3: Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows (CMD):
venv\Scripts\activate

# Step 4: Install the required packages
pip install -r requirements.txt
```

If there's no requirements.txt, you can install Flask manually:

```bash
pip install flask flask_sqlalchemy flask_wtf wtforms email-validator
```

For Timetable Manager with PostgreSQL:
```bash
pip install psycopg2-binary
```

---

## 📁 2. Project Structure

Each project has the following:

```
├── app.py              # Main Flask app
├── models.py           # SQLAlchemy models (if split)
├── templates/          # HTML templates
├── static/             # CSS/JS assets
├── seed.py             # (optional) populate demo data
├── config.py           # (Timetable Manager only)
└── requirements.txt    # dependencies
```

---

## 🧑‍🏫 3. Timetable Manager

A multi-role educational web app with login-based dashboards for admin, teachers, and students.

- Admin can manage users and timetables
- Teachers can view/edit their classes
- Students can see their assigned classes

🛠️ Setup Notes:

- Uses PostgreSQL. In config.py:

  ```python
  SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/timetable_app'
  ```

  You must create this DB first using psql or pgAdmin.

✅ Run it:

```bash
python app.py
```

✅ Seed demo data:

```bash
python seed.py
```

Then login as:

- Admin → admin@example.com / adminpass
- Teacher → teacher1@example.com / teacherpass
- Student → student1@example.com / studentpass

---

## 🍽️ 4. Restaurant Menu Manager

Create, edit, and view menu items. Customers can select multiple dishes and checkout.

🛠️ Uses SQLite by default.

✅ Run it:

```bash
python app.py
```

✅ Seed demo items:

```bash
python seed.py
```

Visit: http://localhost:5000 to see the menu.

---

## 👥 5. Address Book

A simple CRUD app to manage names, email addresses, and phone numbers.

✅ Run it:

```bash
python app.py
```

✅ Seed Australian contact data:

```bash
python seed.py
```

Visit: http://localhost:5000 to see the contact list.

---

## ✨ Tips

- Want to switch from SQLite to PostgreSQL or MySQL? Update SQLALCHEMY_DATABASE_URI in app.config.
- Each project has flash messages and form validation built in.
- Always run Python scripts inside an activated virtual environment.

---

## 🧹 Cleanup

To deactivate the virtual environment:

```bash
deactivate
```

---

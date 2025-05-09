# seed.py
from app import app, db
from app import Person  # adjust if needed
from werkzeug.exceptions import InternalServerError

def seed_people():
    db.drop_all()
    db.create_all()

    demo_people = [
        Person(
            name="Olivia Brown",
            address="12 Collins Street, Melbourne VIC 3000",
            email="olivia.brown@example.com",
            phone="0412 345 678"
        ),
        Person(
            name="Liam Smith",
            address="88 George Street, Sydney NSW 2000",
            email="liam.smith@example.com",
            phone="0401 234 567"
        ),
        Person(
            name="Ava Wilson",
            address="5 St Georges Terrace, Perth WA 6000",
            email="ava.wilson@example.com",
            phone="0423 456 789"
        ),
        Person(
            name="Noah Johnson",
            address="20 King William Street, Adelaide SA 5000",
            email="noah.johnson@example.com",
            phone="0433 987 654"
        ),
        Person(
            name="Isla Taylor",
            address="33 Ann Street, Brisbane QLD 4000",
            email="isla.taylor@example.com",
            phone="0455 321 987"
        )
    ]

    try:
        db.session.add_all(demo_people)
        db.session.commit()
        print("✅ Address book demo data seeded contacts!")
    except Exception as e:
        db.session.rollback()
        raise InternalServerError(f"❌ Error seeding data: {e}")

if __name__ == '__main__':
    with app.app_context():
        seed_people()

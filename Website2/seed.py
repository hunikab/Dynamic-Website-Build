from app import app, db
from app import MenuItem  # Adjust if MenuItem is in a different file/module

def seed_menu():
    db.drop_all()
    db.create_all()

    items = [
        MenuItem(type="Starter", description="Tomato Soup with Garlic Bread", cost=250),
        MenuItem(type="Main", description="Grilled Chicken with Rice", cost=550),
        MenuItem(type="Main", description="Beef Burger with Fries", cost=600),
        MenuItem(type="Dessert", description="Chocolate Lava Cake", cost=300),
        MenuItem(type="Drink", description="Fresh Passion Juice", cost=150),
        MenuItem(type="Drink", description="Mineral Water (500ml)", cost=80),
    ]

    db.session.add_all(items)
    db.session.commit()
    print("✅ Menu seeded successfully!")

if __name__ == '__main__':
    with app.app_context():
        seed_menu()



from app import app, db
from model import Users, Points, Orders, Products, OrderProducts

with app.app_context():
    db.create_all()
    print("✓ База данных создана успешно в файле ex1.db")

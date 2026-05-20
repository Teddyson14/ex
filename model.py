from database import db

class Users(db.Model):   
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role = db.Column(db.String(300), nullable=False)
    fio = db.Column(db.String(300), nullable=False)   
    login = db.Column(db.String(300), nullable=False, unique=True)
    password = db.Column(db.String(300), nullable=False)  

class Points(db.Model):   
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)   
    address = db.Column(db.String(500), nullable=False, unique=True)

class Orders(db.Model):   
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)      
    date_create = db.Column(db.DateTime, nullable=False)   
    date_end = db.Column(db.DateTime, nullable=False)
    point_id = db.Column(db.Integer, db.ForeignKey('points.id'), nullable=False)
    user_id = db.Column(db.String(320), db.ForeignKey('users.id'), nullable=False)
    recive_code = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(300), nullable=False)

class Products(db.Model):   
    article = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    unit = db.Column(db.String(100), nullable=False)   
    price = db.Column(db.Integer, nullable=False)
    supplier = db.Column(db.String(300), nullable=False)
    manufacturer = db.Column(db.String(300), nullable=False)
    category = db.Column(db.String(300), nullable=False)
    discount = db.Column(db.Integer)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500))
    src_img = db.Column(db.String(100))

class OrderProducts(db.Model):   
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)   
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)   
    product_id = db.Column(db.String(100), db.ForeignKey('products.article'), nullable=False)   
    amount = db.Column(db.Integer, nullable=False)

    
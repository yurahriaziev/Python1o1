from flask_sqlalchemy import SQLAlchemy
from config import app

db = SQLAlchemy(app)

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(20), nullable=False)
    pictures = db.Column(db.String(200), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'make': self.make,
            'model': self.model,
            'price': self.price,
            'color': self.color,
            'pictures': self.pictures.split(',') if self.pictures else []
        }
    
with app.app_context():
    db.create_all()

def get_cars():
    cars = Car.query.all()
    return [car.to_dict() for car in cars]

def add_car(make, model, price, color, picture):
    new_car = Car(make=make, model=model, price=price, color=color, pictures=picture)
    db.session.add(new_car)
    db.session.commit()

def remove_car(car):
    db.session.delete(car)
    db.session.commit()

def get_car(car_id):
    car = Car.query.get(car_id)
    return car
from config import app 
from flask_sqlalchemy import SQLAlchemy 
import bcrypt

db=SQLAlchemy(app)

class Car(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    make=db.Column(db.String(20),nullable=False)
    model=db.Column(db.String(25),nullable=False)
    price=db.Column(db.Integer,nullable=False)
    year=db.Column(db.Integer,nullable=False)
    color=db.Column(db.String(20),nullable=False)
    picture=db.Column(db.String(200),nullable=False)

    def to_dict(self):
        return {
            'id':self.id,
            'make':self.make,
            'model':self.model,
            'price':self.price,
            'year':self.year,
            'color':self.color,
            'pictures':self.picture.split(',') if self.picture else []
        }
    

def add_car(make,model,price,color,year,picture):
    new_car= Car(make=make,model=model,price=price,color=color,year=year,picture=picture)
    db.session.add(new_car)
    db.session.commit()
def get_cars():
    cars= Car.query.all()
    to_send= []
    for car in cars:
        a = car.to_dict()
        to_send.append(a)
    return to_send
def remove_car(id):
    car=Car.query.get(id)
    if car:
        db.session.delete(car)
        db.session.commit()
    else:
        return f"No car found with ID {id}"
def get_car(id):
    car=Car.query.get(id)
    if car:
        return car
    else:
        return False
    
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    first=db.Column(db.String(50),nullable=False)
    last=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(120),nullable=False)
    password_hash=db.Column(db.String(200),nullable=False)

    def set_password(self,password):
        self.password_hash=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password_hash)
    
def add_user(first,last,email,password):
    new_user= User(first=first, last=last, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
with app.app_context():
    db.create_all()
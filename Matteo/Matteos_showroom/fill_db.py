cars = [
    # {"make": "Lamborghini", "model": "Aventador", "year": 2022, "price": 500000, "color": "Yellow", "pictures": "default.png"},
    # {"make": "Ferrari", "model": "488 Pista", "year": 2020, "price": 450000, "color": "Red", "pictures": "default.png"},
    # {"make": "McLaren", "model": "720S", "year": 2021, "price": 350000, "color": "Orange", "pictures": "default.png"},
    # {"make": "Bugatti", "model": "Chiron", "year": 2023, "price": 3000000, "color": "Blue", "pictures": "default.png"},
    # {"make": "Porsche", "model": "911 GT3 RS", "year": 2022, "price": 250000, "color": "Green", "pictures": "default.png"},
    # {"make": "Aston Martin", "model": "Valkyrie", "year": 2023, "price": 3000000, "color": "Silver", "pictures": "default.png"},
    # {"make": "Koenigsegg", "model": "Jesko", "year": 2023, "price": 3200000, "color": "White", "pictures": "default.png"},
    # {"make": "Pagani", "model": "Huayra", "year": 2021, "price": 2500000, "color": "Purple", "pictures": "default.png"},
    # {"make": "Rolls-Royce", "model": "Phantom", "year": 2022, "price": 450000, "color": "Black", "pictures": "default.png"},
    {"make": "Bentley", "model": "Continental GT", "year": 2022, "price": 250000, "color": "Blue", "pictures": "default.png"},
]
from config import app 
from db import add_car,get_cars,Car,db,User


with app.app_context():
    # cars=get_cars()
    # for car in cars:
    #     print(car['model'],type(car['price']))
    #    add_car(car['make'],car['model'],car['price'],car['color'],car['year'],car['pictures'])
    # car=Car.query.filter_by(model='SF-90').first()
    # db.session.delete(car)
    # db.session.commit()
    users=User.query.all()
    print(users)
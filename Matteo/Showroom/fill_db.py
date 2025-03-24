'''
File meant to add test cars to the database.
'''

from db import add_car
from config import app

# add these cars to the databas
cars = [
    {"make": "Lamborghini", "model": "Hurracan", "price": 500000, "color": "White", "pictures": "default.png"},
    # {"make": "Ferrari", "model": "488 Pista", "price": 450000, "color": "Red", "pictures": "default.png"},
    # {"make": "McLaren", "model": "720S", "price": 350000, "color": "Orange", "pictures": "default.png"},
    # {"make": "Bugatti", "model": "Chiron", "price": 3000000, "color": "Blue", "pictures": "default.png"},
    {"make": "Porsche", "model": "911", "price": 250000, "color": "Red", "pictures": "default.png"},
    # {"make": "Aston Martin", "model": "Valkyrie", "price": 3000000, "color": "Silver", "pictures": "default.png"},
    # {"make": "Koenigsegg", "model": "Jesko", "price": 3200000, "color": "White", "pictures": "default.png"},
    # {"make": "Pagani", "model": "Huayra", "price": 2500000, "color": "Purple", "pictures": "default.png"},
    # {"make": "Rolls-Royce", "model": "Phantom", "price": 450000, "color": "Black", "pictures": "default.png"},
    {"make": "Bentley", "model": "Continental GT", "price": 250000, "color": "Dark Blue", "pictures": "default.png"},
]

with app.app_context():
    # looping through each car dictionary and add it to the database
    for c in cars:
        add_car(c['make'], c['model'], c['price'], c['color'], c['pictures'])


from flask import Flask, render_template, url_for, request, redirect
import os
from config import app
from db import Car, add_car, get_cars, remove_car, get_car

car1 = {
    'name':'ferrari',
    'make':'Ferrari',
    'model':'F1',
    'price':15000000,
    'color':'red',
    'pictures':['ferrari-1.jpeg', 'ferrari-2.jpeg']
}

car2 = {
    'name':'mercedes',
    'make':'Mercedes',
    'model':'F1',
    'price':15000000,
    'color':'black',
    'pictures':['mercedes-1.jpeg', 'mercedes-2.jpeg']
}

car3 = {
    'name':'redbul',
    'make':'RedBull',
    'model':'F1',
    'price':15000000,
    'color':'black',
    'pictures':['redbull-1.jpeg', 'redbull-2.jpeg']
}

# cars = get_cars()

@app.route('/')
@app.route('/inventory', methods=['GET'])
def inventory():
    query = request.args.get('search', '').strip().lower()
    max_price = request.args.get('max_price', '').strip() # new
    cars = get_cars()

    filtered_cars = []
    # print(query)
    if query:
        for car in cars:
            if (query in car['make'].lower() or query in car['model'].lower() or query in car['color'].lower()):
                filtered_cars.append(car)
    else:
        filtered_cars = cars

    if max_price:
        try:
            max_price = float(max_price)
            temp_cars = []
            for car in filtered_cars:
                if car['price'] <= max_price:
                    temp_cars.append(car)
            
            filtered_cars = temp_cars
        except ValueError:
            pass

    return render_template('inventory.html', cars=filtered_cars, searh_query=query)
# @app.route('/home')
# def home():
#     cars_info = []
#     cars = get_cars()
#     for car in cars:
#         car_info = {'picture':car.get('pictures')[0], 'make':car.get('make'), 'model':car.get('model')}
#         cars_info.append(car_info)
#     print(cars_info) # log
#     return render_template('homepage.html', cars_info=cars_info)

@app.route('/car-details/<car_id>')
def car_details(car_id):
    car = get_car(car_id)
    if car:
        car_details = car.to_dict()
        if not car_details:
            return render_template('car_not_found.html')
        
        return render_template('car_details.html', car_info=car_details)
        
    return render_template('car_not_found.html')


@app.route('/new-car',methods=['POST','GET'])
def new_car():
    if request.method=='POST':
        

        form=request.form
        make=form['make']
        model=form['model']
        price=form['price'].strip()
        color=form['color']
        # year=form['year']
        year = '2025'

        file=request.files['photo']
        _,ext=os.path.splitext(file.filename)
        new_name= f'{make.lower()}-{model.lower()}{ext}'
        print(new_name)
        file_path=os.path.join('/Users/yuriihriaziev/Documents/Programming/Python1o1/Matteo/Showroom/static/images',new_name)
        file.save(file_path)

        print(price, type(price))
        add_car(make,model,price,color,new_name)
        
        return redirect(url_for('inventory'))
    return render_template('add_car.html')

@app.route('/delete-car/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    car = Car.query.get(car_id)

    if car:
        remove_car(car)
        return redirect(url_for('inventory'))
    else:
        return render_template('car_not_found.html')

if __name__ == "__main__":
    app.run(debug=True)
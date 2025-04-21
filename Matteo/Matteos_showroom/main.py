# Website structure

#   Routes
# Homepage
# - Welcome message
# - Recent new cars
# - Reviews
# - Sidebar

# Inventory
# - View each car
# - Car quantity

# Dealership locations
# - Locations on map

from flask import Flask, render_template, url_for, request, redirect
import os 
from config import app 
from db import add_car, get_cars, remove_car, get_car, add_user, User

car1= {
    'name':'mercedes',
    'year':'2021',
    'color':'#000000',
    'make':'Mercedes',
    'model':'W12',
    'price':20000000,
    'pictures':['mercedes-1.jpeg','mercedes-2.jpeg','mercedes-3.jpeg']
}
car2= {
    'name':'redbull',
    'year':'2021',
    'color':'#0000ff',
    'make':'Red Bull',
    'model':'RB16B',
    'price':20000000,
    'pictures': ['redbull-1.jpeg','redbull-2.jpeg','redbull-3.jpeg']
}
car3= {
    'name':'ferrari',
    'year':'2022',
    'color':'#ff0000',
    'make':'Ferrari',
    'model':'SF-22',
    'price':20000000,
    'pictures': ['ferrari-1.jpeg','ferrari-2.jpeg','ferrari-3.jpeg']
}
cars= [car1,car2,car3]

''' Routes '''
# Formula for route creation
# @app.route('/route-name')
# def route_name():
#   ...
@app.route('/')
@app.route('/homepage')
def homepage():
    print(cars)
    cars_info= []
    for car in cars:
        car_info= {'make':car['make'],
                     'model':car['model'],
                     'picture':car['pictures'][0]
                    }
        cars_info.append(car_info)

    return render_template('homepage.html',cars_info=cars_info)

@app.route('/inventory',methods=['GET'])
def inventory():
    inv_cars = get_cars() + cars

    query=request.args.get("search",'').strip().lower()

    budget=request.args.get("budget",'').strip()
    # print(budget)
    results=[]
    if query:
        for car in inv_cars:
            if (query in car['make'].lower() or query in car['model'].lower() or query in car['color'].lower()):
                results.append(car)
    else:
        results=inv_cars
    
    if budget:
        try:
            # budget=int(budget.replace(',',''))
            # print(type(budget))
            budget=float(budget)
            temp_cars=[]
            for car in results:
                if car['price']<=budget:
                    temp_cars.append(car)
            results=temp_cars
        except ValueError:
            pass

    return render_template('inventory.html',cars=results,search_query=query)

@app.route('/locations')
def locations():
    return render_template('locations.html')

@app.route('/car/<car_id>')
def car(car_id):
    car= get_car(car_id)
    if car:
        car_details= car.to_dict()
        return render_template('car.html',car=car_details)
    
    return render_template('car_not_found.html')

@app.route('/new-car',methods=['POST','GET'])
def new_car():
    if request.method=='POST':
        

        form=request.form
        make=form['make']
        model=form['model']
        price=form['price']
        print(type(price))
        color=form['color']
        year=form['year']

        file=request.files['file']
        _,ext=os.path.splitext(file.filename)
        new_name= f'{make.lower()}-{model.lower()}{ext}'
        print(new_name)
        file_path=os.path.join('/Users/matteoventuracci/Python Course/projects/Matteos_showroom/static/images',new_name)
        file.save(file_path)

        add_car(make,model,price,color,year,new_name)
        
        return redirect(url_for('inventory'))
    return render_template('new_car.html')

@app.route('/delete-car/<int:id>')
def delete_car(id):
    if id:
        remove_car(id)
        return redirect(url_for('inventory'))
    else:
        return render_template('car_not_found.html')


@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        form=request.form
        first=form['first']
        last=form['last']
        email=form['email']
        password=form['password']
        add_user(first,last,email,password)
        return redirect(url_for('login'))
    return render_template('sign_up.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        user=User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            print('Logged in successfully!')
        else:
            print('Login failed.')

    return render_template('login.html')

if __name__=='__main__':
    app.run(debug=True)
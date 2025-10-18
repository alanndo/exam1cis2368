import flask
import mysql.connector
import creds
from mysql.connector import Error
from sql import create_connection
from sql import execute_query
from sql import execute_read_query
from flask import jsonify
from flask import request

app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show errors in browser

myCreds = creds.Creds()
conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

tableCars = """
CREATE TABLE IF NOT EXISTS cars(
id INT AUTO_INCREMENT,
make VARCHAR(255) NOT NULL,
model VARCHAR(255) NOT NULL,
color VARCHAR(255) NOT NULL,
year int,
costperday int,
renter VARCHAR(255) NOT NULL,
PRIMARY KEY (id)
)
"""
execute_query(conn,tableCars)

add_cars_query = """
INSERT INTO cars (make, model, color, year, costperday, renter)
VALUES
    ('honda', 'civic', 'white','2001','10000','alan do'),
    ('toyota', 'rav4', 'blue','2004,'20000','bre fuentes'),
    ('mercedes', 'randomname', 'green','2004','30000','koshi fujita'),
    ('lambo', 'randomlambo', 'black','2002','40000','brian choi'),
    ('acura', 'randomacura', 'purple','2001','50000','william nguyen')
"""
execute_query(conn, add_cars_query)


@app.route('/api/car', methods=['POST']) # add cars as POST:
def add_addcar():          
    cars = execute_read_query(conn,tableCars)

    request_data = request.get_json()   
    newid = request_data['id']   
    newMake = request_data['make']
    newModel = request_data['model']
    newColor = request_data['color']
    newYear = request_data['year']   
    newCostperday = request_data['costperday']
    newrenter = request_data['renter']


    cars.append({'id': newid, 'make': newMake, 'model': newModel, 'color': newColor, 'year': newYear, 'costperday': newCostperday, 'renter': newrenter})
    execute_query(conn, tableCars)
    return 'Added Car'

@app.route('/api/PUT/grades', methods=['PUT']) #update car
def api_updatecar():
    cars = execute_read_query(conn,tableCars)

    request_data = request.get_json()
    car_id = request_data['id']
    costperday_request = request_data['costperday']

# find the carid and costperday return none or null if return it.
    for i in range(len(car_id) - 1, -1, -1):
        if car_id[i]['id'] == car_id and costperday_request[i]['costperday'] == costperday_request:
            return cars([i])
    else:
        return None


@app.route('/api/car', methods=['GET']) #endpoint to get all the students:
def api_all():
    cars = execute_read_query(conn,tableCars)
    request_data = request.get_json()
    newrenter = request_data['renter']

    #used ai to generate some of this code google

    # if renter in students is null, return the car, if does not return null do not return the car as it is owned.
    for availablecars in cars:
        if newrenter == None:
                #  return cars that are not null and sum of daily revenue of cars

            dailyrevenue = """
            SELECT costperday, renter
            FROM cars
            WHERE renter = IS NOT NULL;
            """
            execute_query(dailyrevenue)
        return jsonify(availablecars)

app.run()

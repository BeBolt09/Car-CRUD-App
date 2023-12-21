from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, Car_schema, Cars_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'naw'}

# @api.route('/data')
# def viewdata():
#     data = get_Car()
#     response = jsonify(data)
#     print(response)
#     return render_template('index.html', data = data)

@api.route('/Cars', methods = ['POST'])
@token_required
def create_Car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    condition = request.json['condition']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(make, model, year, condition, user_token = user_token )
    db.session.add(car)
    db.session.commit()

    response = Car_schema.dump(car)
    return jsonify(response)

@api.route('/Cars', methods = ['GET'])
@token_required
def get_Car(current_user_token):
    a_user = current_user_token.token
    Cars = Car.query.filter_by(user_token = a_user).all()
    response = Cars_schema.dump(Cars)
    return jsonify(response)

@api.route('/Cars/<id>', methods = ['GET'])
@token_required
def get_Car_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        car = Car.query.get(id)
        response = Car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
@api.route('/Cars/<id>', methods = ['POST','PUT'])
@token_required
def update_Car(current_user_token,id):
    car = Car.query.get(id) 
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.condition = request.json['condition']
    car.user_token = current_user_token.token

    db.session.commit()
    response = Car_schema.dump(car)
    return jsonify(response)


# DELETE car ENDPOINT
@api.route('/Cars/<id>', methods = ['DELETE'])
@token_required
def delete_Car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = Car_schema.dump(car)
    return jsonify(response)
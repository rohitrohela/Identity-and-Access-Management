import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
@requires_auth('get:drinks')
def GetDrinks(jwt):
    drinks = [drink.short() for drink in Drink.query.all()]
    return jsonify(
        {
            "Success": True,
            "drinks": drinks
        }
    )


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def GetDrinksDetails(jwt):
    drinks = [drink.long() for drink in Drink.query.all()]
    return jsonify(
        {
            "Success": True,
            "drinks": drinks
        }
    )


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def PostDrink(jwt):
    success = True
    result = ""
    body = request.get_json()
    drink = Drink(
        title=body['title'],
        recipe=str(body['recipe']).replace("'", '"')
    )
    try:
        drink.insert()
        result = drink.long()
    except Exception as e:
        db.session.rollback()
        success = False
    finally:
        db.session.close()
    return jsonify(
        {
            "Success": success,
            "drinks": result
        }
    )


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def PatchDrink(jwt, drink_id):
    success = True
    result=[]
    drink = Drink.query.filter_by(id=drink_id).one_or_none()
    if drink is None:
        raise abort(404, "No Drink Found")

    body = request.get_json()
    drink.title = body['title']
    if 'recipe' in body:
        drink.recipe = str(body['recipe']).replace("'", '"')

    try:
        drink.update()
        result.append(drink.long())
    except Exception as e:
        db.session.rollback()
        success = False
    finally:
        db.session.close()
    return jsonify(
        {
            "Success": success,
            "drinks": result
        }
    )


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def DeleteDrink(jwt, drink_id):
    success = True
    drink = Drink.query.filter_by(id=drink_id).one_or_none()
    if drink is None:
        raise abort(404, "No Drink Found")
    try:
        drink.delete()
    except Exception as e:
        db.session.rollback()
        success = False
    finally:
        db.session.close()
    return jsonify(
        {
            "Success": success,
            "delete": drink_id
        }
    )


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable",
        "description": error.description,
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found",
        "description": error.description
    }), 404


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def handle_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error,
    }), error.status_code

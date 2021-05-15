
# -*- coding: utf-8 -*-
from flasgger.utils import swag_from
from flask import Blueprint
from flask import Response
from flask import request
from flask import jsonify
import json
import os
from api.src.postgre import Postgres

violence_blueprint = Blueprint('violence_blueprint', __name__, url_prefix="/violence")


@violence_blueprint.route("/get", methods=['GET'])
@swag_from('get_all.yml')
def list_all():
  postgre = Postgres()
  postgre.open()
  results = postgre.getVeolance(0);
  postgre.close()
  violences = fromResultsToJson(results)
  return Response(json.dumps(violences),
                      status=200, mimetype='application/json')


@violence_blueprint.route("/get/<quantidade>", methods=['GET'])
@swag_from('get_size.yml')
def list(quantidade):
  postgre = Postgres()
  postgre.open()
  results = postgre.getVeolance(quantidade);
  postgre.close()
  violences = fromResultsToJson(results)
  return Response(json.dumps(violences),
                      status=200, mimetype='application/json')

@violence_blueprint.route("/get/by/type/<type>", methods=['GET'])
@swag_from('get_type_all.yml')
def list_type_all(type):
  postgre = Postgres()
  postgre.open()
  results = postgre.getViolenceByType(type, 0);
  postgre.close()
  violences = fromResultsToJson(results)
  return Response(json.dumps(violences),
                      status=200, mimetype='application/json')


@violence_blueprint.route("/get/by/type/<type>/<quantidade>", methods=['GET'])
@swag_from('get_type_size.yml')
def list_type(type, quantidade):
  postgre = Postgres()
  postgre.open()
  results = postgre.getViolenceByType(type, quantidade);
  postgre.close()
  violences = fromResultsToJson(results)
  return Response(json.dumps(violences),
                      status=200, mimetype='application/json')


@violence_blueprint.route("/type/", methods=['GET'])
@swag_from('get_type.yml')
def type():
  postgre = Postgres()
  postgre.open()
  results = postgre.getType();
  postgre.close()
  types = fromResultsToType(results)
  return Response(json.dumps(types),
                      status=200, mimetype='application/json')

@violence_blueprint.route("/amount/lost", methods=['GET'])
@swag_from('get_amount.yml')
def amount():
  postgre = Postgres()
  postgre.open()
  results = postgre.getAmountOfLost();
  postgre.close()
  return Response(json.dumps({'amount': str(results[0][0])}),
                      status=200, mimetype='application/json')

@violence_blueprint.route("/by/neighborhood", methods=['GET'])
@swag_from('get_neighborhood.yml')
def neighborhood():
  postgre = Postgres()
  postgre.open()
  results = postgre.getViolenceGroupByNeighborhood();
  postgre.close()
  neighborhoods = fromResultsToNeighborhood(results)
  return Response(json.dumps(neighborhoods),status=200, mimetype='application/json')

@violence_blueprint.route("/by/type", methods=['GET'])
@swag_from('get_by_type.yml')
def agregaPorTipo():
  postgre = Postgres()
  postgre.open()
  results = postgre.getViolenceGroupByType();
  postgre.close()
  types = fromResultsToNeighborhood(results)
  return Response(json.dumps(types),
                      status=200, mimetype='application/json')


@violence_blueprint.route("/lost/gender", methods=['GET'])
@swag_from('get_gender.yml')
def gender():
  postgre = Postgres()
  postgre.open()
  results = postgre.getLostBySex();
  print(results)
  masc = results[0][1] /(results[0][1] + results[1][1])
  fem  = results[1][1] / (results[0][1] + results[1][1])
  postgre.close()
  return Response(json.dumps({'masculino': masc,'feminino': fem}),
                      status=200, mimetype='application/json')

def fromResultsToJson(results):
  violences = []
  for result in results: 
    violence = {
      'title': result[0],
      'latitude': str(result[1]),
      'longitude': str(result[2]),
      'event_data': result[3].strftime('%Y-%m-%d %H:%M:%S'),
      'bulletin_occurrence': result[4],
      'damage_value': str(result[5]),
      'neighborhood': result[6],
      'county': result[7],
      'name': result[8],
      'type': str(result[9]),
      'description': result[10],
      'sex': str(result[11]),
      'address': result[12],
      'source': result[13],
      'day_of_week': result[14],
      'shift': result[15],
      'source': result[16]
    }
    violences.append(violence)
  return violences
  
def fromResultsToType(results):
  types = []
  for result in results: 
    type = {
      'id': str(result[0]),
      'name': result[1]
    }
    types.append(type)
  return types

def fromResultsToNeighborhood(results):
  neighborhood = []
  for result in results: 
    n = {      
      'name': result[0],
      'amount': str(result[1]),
    }
    neighborhood.append(n)
  return neighborhood
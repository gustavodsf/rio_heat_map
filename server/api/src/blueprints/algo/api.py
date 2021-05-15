# -*- coding: utf-8 -*-
from flasgger.utils import swag_from
from flask import Blueprint
from flask import Response
from flask import request
from flask import jsonify
import json
import os
from api.src.postgre import Postgres
from api.src.kde import KDE
from api.src.machine_learnning  import MachineLearnning

algo_blueprint = Blueprint('algo_blueprint', __name__, url_prefix="/algo")

@algo_blueprint.route("/kde", methods=['GET'])
@swag_from('get_kde.yml')
def run_kde():
  postgre = Postgres()
  postgre.open()
  results = postgre.getVeolance(1000);
  postgre.close()
  violences = fromResultsToJson(results)
  kde = KDE()
  result = kde.run(violences)
  return Response(json.dumps(result),
                      status=200, mimetype='application/json')


@algo_blueprint.route("/ml", methods=['GET'])
@swag_from('get_ml.yml')
def run_ml():
  postgre = Postgres()
  postgre.open()
  results = postgre.getVeolance(3000);
  postgre.close()
  violences = fromResultsToJson(results)
  ml = MachineLearnning()
  result = ml.run(violences)
  return Response(json.dumps(result),
                      status=200, mimetype='application/json')


@algo_blueprint.route("/kde/<tipo>", methods=['GET'])
@swag_from('get_type_kde.yml')
def run_kde_filtered(tipo):
  postgre = Postgres()
  postgre.open()
  results = postgre.getVeolanceFilterByType(1000, tipo);
  postgre.close()
  violences = fromResultsToJson(results)
  kde = KDE()
  result = kde.run(violences)
  return Response(json.dumps(result),
                      status=200, mimetype='application/json')


@algo_blueprint.route("/ml/<tipo>", methods=['GET'])
@swag_from('get_type_ml.yml')
def run_ml_filtered(tipo):
  postgre = Postgres()
  postgre.open()
  results = postgre.getVeolanceFilterByType(3000, tipo);
  postgre.close()
  violences = fromResultsToJson(results)
  ml = MachineLearnning()
  result = ml.run(violences)
  return Response(json.dumps(result),
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
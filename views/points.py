import calendar
import datetime
import json
import logging
import logging.handlers
import os
import requests
import sys
import urllib.request
import uuid

from dateutil.parser import parse
from schematics.exceptions import ValidationError


from flask import Flask, jsonify, request, redirect
from flask import Blueprint

from .schema.structure import Points

from api.points_mgmt import get_user_points_balance
from api.points_mgmt import save_user_points
from api.points_mgmt import consume_user_points

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# create logger 
logger = logging.getLogger('rewards_mgmt')
logger.setLevel(logging.INFO)

points = Blueprint('points', __name__)

@points.route('/transaction/add_points/<user_id>/', methods=['POST'])
def add_user_points(user_id):
	''' 
		add transaction by payer, timestamp 
		{ "payer": "DANNON", "points": 1000, "timestamp": "2020-11-02T14:00:00Z" }
	'''

	schema = None
	try:
		record = json.loads(request.data)['inputs']
		schema = Points(record)
		schema.validate()

	except ValidationError as ve:
		return ve.message, 400

	except Exception as ex:
		logger.error(f'Exception in add_points {str(ex.args)}')


	tran_id = uuid.uuid4()
	version = int(calendar.timegm(datetime.datetime.utcnow().timetuple()))

	# store points
	user_points = schema.to_primitive()
	user_points.update({
		'timestamp': parse(user_points['timestamp']),
		'transaction_id': str(tran_id),
		'version': version
	})
    # save points
	save_user_points(user_id, user_points)

	logger.info(f'add_user_points success with user: {user_id}:{tran_id}')

	return {
		'user_id': user_id,
		'transaction_id': tran_id,
		'version': version
	}, 200



@points.route('/transaction/spend_points/<user_id>/', methods=['POST'])
def spend_user_points(user_id):
	''' spend points '''

	if user_id:
		record = json.loads(request.data)['inputs']
		return consume_user_points(user_id, record['points'])

	return {'points': 0}

@points.route('/transaction/get_points/<user_id>/', methods=['GET'])
def get_points_balance(user_id):
	''' get points balance '''

	if user_id:
		return {"points": get_user_points_balance(user_id)}

	return {"points": {}}

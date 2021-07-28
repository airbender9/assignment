import heapq
import logging
import json

from copy import copy
from dateutil.parser import parse

from .RewardPoints import RewardPoints

# create logger 
logger = logging.getLogger('rewards_mgmt')
logger.setLevel(logging.INFO)

# global variable
user_points = {}

def iterator(heap):
	''' iterate heap '''

	heap = copy(heap)
	try:
		while True:
			yield heapq.heappop(heap)
	except IndexError:
		return

def save_user_points(user_id:str, points:RewardPoints):
	''' 
		save user points 

		consolidation logic: as soon as find points on same day, merge them
	'''

	global user_points
	global offset_points

	user_records = user_points[user_id] if user_id in user_points else []
	# consolidate points on the same date (use earlier timestamp)
	merged = None
	for rec in iterator(user_records):
		if rec == RewardPoints(points['timestamp'], points):
			rec.val['points'] += points['points']
			if rec.key > points['timestamp']:
				rec.key = points['timestamp']
				rec.val['timestamp'] = points['timestamp']
			merged = True

			# re-sort it
			heapq.heapify(user_records)
			break

	try:
		if not merged:
			heapq.heappush(user_records, RewardPoints(points['timestamp'], points))

		# save user records for a user_id
		user_points[user_id] = user_records

	except Exception as ex:
		logger.error(f'Exception in save_user_points {str(ex.args)}')

	finally:
		return user_records


def get_user_points_balance(user_id:str):
	''' get user points '''

	global user_points

	points_balance = {}
	try:
		if user_id in user_points:
			for rec in iterator(user_points[user_id]):
				record = rec.toJSON()
				if record['payer'] in points_balance:
					points_balance[record['payer']] += record['points']
				else:
					points_balance[record['payer']] = record['points']

	except Exception as ex:
		logger.error(f'Exception in get_user_points_balance {str(ex.args)}')

	finally:
		return points_balance

def consume_user_points(user_id:str, total_points:int):
	''' consume user points '''

	global user_points

	spent_points = []
	try:
		for user_id, reward_points in user_points.items():
			modified_points = []
			for record in iterator(reward_points):
				if record.val['points'] > 0 and total_points > 0:
					offset = record.val['points'] if record.val['points'] <= total_points else total_points
					spent_points.append({'payer': record.val['payer'], 'points': -1.0 * offset })
					record.val['points'] -= offset
					total_points = total_points - offset
			
				heapq.heappush(modified_points, RewardPoints(record.val['timestamp'],\
						{ 'payer': record.val['payer'], 'points': record.val['points'], 'timestamp': record.val['timestamp']}))

			user_points[user_id] = modified_points
	except Exception as ex:
		logger.error(f'Exception in consume_user_points {str(ex.args)}')

	finally:
		return {'points': spent_points}

def clear_user_points(user_id:str):
	''' clear user points '''

	global user_points

	if user_id and user_id in user_points:
		del user_points[user_id]

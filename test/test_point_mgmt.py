import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from api.RewardPoints import RewardPoints

from api.points_mgmt import get_user_points_balance
from api.points_mgmt import save_user_points
from api.points_mgmt import consume_user_points
from api.points_mgmt import clear_user_points

from dateutil.parser import parse

class RewardPointsMgmtTest(unittest.TestCase):

	def test_save_user_points(self):
		''' test save user points '''

		user_id = '1111'
		clear_user_points(user_id)

		point = { "payer": "DANNON", "points": 1000, "timestamp": parse("2020-11-02T14:00:00Z") }
		resultset = save_user_points(user_id, point)

		point = { "payer": "UNILEVER", "points": 200, "timestamp": parse("2020-10-31T11:00:00Z") }
		resultset = save_user_points(user_id, point)

		# assert that result is sorted by timestamp
		top_item = resultset[0]
		self.assertEqual(RewardPoints, type(top_item))

		expected = 'UNILEVER'
		self.assertEqual(expected, top_item.toJSON()['payer'])


	def test_merge_points_by_date_payer(self):
		''' test merge points '''

		user_id = '1111'

		clear_user_points(user_id)

		point = { "payer": "DANNON", "points": -200, "timestamp": parse("2020-10-31T15:00:00Z")}
		resultset = save_user_points(user_id, point)

		point = { "payer": "DANNON", "points": 300, "timestamp": parse("2020-10-31T10:00:00Z")}
		resultset = save_user_points(user_id, point)

		expected = 100
		self.assertEqual(expected, resultset[0].toJSON()['points'])


	def test_reward_points_ordering(self):
		''' test reward points ordering '''

		user_id = '1111'
		points = [
			{ "payer": "DANNON", "points": 1000, "timestamp": parse("2020-11-02T14:00:00Z") },
			{ "payer": "UNILEVER", "points": 200, "timestamp": parse("2020-10-31T11:00:00Z") },
			{ "payer": "DANNON", "points": -200, "timestamp": parse("2020-10-31T15:00:00Z") },
			{ "payer": "MILLER COORS", "points": 10000, "timestamp": parse("2020-11-01T14:00:00Z") },
			{ "payer": "DANNON", "points": 300, "timestamp": parse("2020-10-31T10:00:00Z") }
		]

		clear_user_points(user_id)
		for reward_point in points:
			resultset = save_user_points(user_id, reward_point)

		# one reward point merged due to offset
		self.assertEqual(4, len(resultset))
		self.assertEqual("DANNON", resultset[0].toJSON()['payer'])
		self.assertEqual(100, resultset[0].toJSON()['points'])

	def test_get_user_points_balance(self):
		''' test get user points balance '''

		user_id = '1111'
		points = [
			{ "payer": "DANNON", "points": 1000, "timestamp": parse("2020-11-02T14:00:00Z") },
			{ "payer": "UNILEVER", "points": 200, "timestamp": parse("2020-10-31T11:00:00Z") },
			{ "payer": "DANNON", "points": -200, "timestamp": parse("2020-10-31T15:00:00Z") },
			{ "payer": "MILLER COORS", "points": 10000, "timestamp": parse("2020-11-01T14:00:00Z") },
			{ "payer": "DANNON", "points": 300, "timestamp": parse("2020-10-31T10:00:00Z") }
		]

		clear_user_points(user_id)
		for reward_point in points:
			resultset = save_user_points(user_id, reward_point)

		# get user balance
		point_balance = get_user_points_balance(user_id)

		# assert type
		self.assertEqual(dict, type(point_balance))

		# assert keys
		self.assertEquals(set(['DANNON', 'MILLER COORS', 'UNILEVER']), set(point_balance.keys()))

		# assert values
		self.assertEquals(1100, point_balance['DANNON'])
		self.assertEquals(200, point_balance['UNILEVER'])


	def test_consume_user_points(self):
		''' test consume user points '''

		user_id = '1111'
		points = [
			{ "payer": "DANNON", "points": 1000, "timestamp": parse("2020-11-02T14:00:00Z") },
			{ "payer": "UNILEVER", "points": 200, "timestamp": parse("2020-10-31T11:00:00Z") },
			{ "payer": "DANNON", "points": -200, "timestamp": parse("2020-10-31T15:00:00Z") },
			{ "payer": "MILLER COORS", "points": 10000, "timestamp": parse("2020-11-01T14:00:00Z") },
			{ "payer": "DANNON", "points": 300, "timestamp": parse("2020-10-31T10:00:00Z") }
		]

		clear_user_points(user_id)
		for reward_point in points:
			resultset = save_user_points(user_id, reward_point)

		# spend 5000 points
		spent = consume_user_points(user_id, 5000)

		expected = [
			{"payer": "DANNON", "points": -100 },
			{"payer": "UNILEVER", "points": -200 },
			{"payer": "MILLER COORS", "points": -4700 }
		]

		for payer in ['DANNON', 'MILLER COORS', 'UNILEVER']:
			consumed_rec = list(filter(lambda x: x['payer'] == payer, spent['points']))
			expected_rec = list(filter(lambda x: x['payer'] == payer, expected))
			self.assertEquals(expected_rec[0]['points'], consumed_rec[0]['points'])

	def test_remaining_balance(self):
		''' test remaining point balance '''

		user_id = '1111'
		points = [
			{ "payer": "DANNON", "points": 1000, "timestamp": parse("2020-11-02T14:00:00Z") },
			{ "payer": "UNILEVER", "points": 200, "timestamp": parse("2020-10-31T11:00:00Z") },
			{ "payer": "DANNON", "points": -200, "timestamp": parse("2020-10-31T15:00:00Z") },
			{ "payer": "MILLER COORS", "points": 10000, "timestamp": parse("2020-11-01T14:00:00Z") },
			{ "payer": "DANNON", "points": 300, "timestamp": parse("2020-10-31T10:00:00Z") }
		]

		clear_user_points(user_id)
		for reward_point in points:
			resultset = save_user_points(user_id, reward_point)

		# spend 5000 points
		spent = consume_user_points(user_id, 5000)

		expected = {
			"DANNON": 1000,
			"UNILEVER": 0,
			"MILLER COORS": 5300 
		}

		# get user balance
		point_balance = get_user_points_balance(user_id)

		for payer in ['DANNON', 'MILLER COORS', 'UNILEVER']:
			self.assertEqual(expected[payer], point_balance[payer])

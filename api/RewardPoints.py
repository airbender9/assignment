import datetime
import json
import heapq

def converter(o):
	''' convert date '''

	if isinstance(o, datetime.datetime):
		return o.__str__()

class RewardPoints(object):

	def __init__(self, key:int ,val: object):
		''' constructor '''

		self.key = key
		self.val = val

	def __repr__(self):
		''' stringified object '''

		return json.dumps(self.val, default=converter, indent=4)

	def __lt__(self, other):
		return self.key < other.key

	def __eq__(self, other):
		''' assume multiple reward points on day should be consolidated '''

		return (self.key.date() == other.key.date() and\
				self.val['payer'] == other.val['payer'])

	def __str__(self):
		''' string '''

		return str("{} : {}".format(self.key, self.val))

	def toJSON(self):
		''' json object '''

		return json.loads(self.__repr__())

import re
  
from schematics.models import Model
from schematics.types import BooleanType
from schematics.types import DecimalType
from schematics.types import IntType
from schematics.types import StringType
from schematics.types import DateTimeType
from schematics.types.compound import ModelType, ListType
from schematics.exceptions import ValidationError


class Points(Model):
	''' points model '''

	payer = StringType(required=True)
	points = IntType(required=True)
	timestamp = StringType(required=True)

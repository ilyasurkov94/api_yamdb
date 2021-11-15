import datetime
from rest_framework.exceptions import ValidationError


def my_year_validator(value):
    if value < 0 or value > datetime.datetime.now().year:
        raise ValidationError(('%(value)s is not a correcrt year!'),
                              params={'value': value},
                              )

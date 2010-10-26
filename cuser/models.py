from django.db import models

# TODO Add group function in shortening
class GroupProfile ( models.Model ):
    income = models.DecimalField ( max_digits = 10, decimal_places = 2 )
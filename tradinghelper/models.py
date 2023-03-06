from django.db import models

# Create your models here.
class Record(models.Model):
    strategy_type = models.CharField(max_length=10)
    symbol = models.CharField(max_length=10)
    benefit = models.FloatField(default=0)
    params = models.CharField(max_length=100)
    def __str__(self):
        return self.strategy_type
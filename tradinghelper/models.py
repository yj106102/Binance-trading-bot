from django.db import models

# Create your models here.
class Record(models.Model):
    strategy_type = models.CharField(max_length=10)
    # 전략 종류(Rsi 등)
    symbol = models.CharField(max_length=10)
    # 거래 종목
    benefit = models.FloatField(default=0)
    # 손익
    params = models.CharField(max_length=100)
    # 파라미터
    def __str__(self):
        return str(self.strategy_type)
    
from django.db import models

class BmfXrpUsdtDaily(models.Model):
    unix = models.BigIntegerField(primary_key=True)  
    date = models.DateTimeField()                   
    symbol = models.CharField(max_length=255)       
    open = models.FloatField()                      
    high = models.FloatField()                      
    low = models.FloatField()                       
    close = models.FloatField()                     
    volume_xrp = models.FloatField()                
    volume_usdt = models.FloatField()               
    trade_count = models.IntegerField()             

    class Meta:
        db_table = 'bmf_xrpusdt_daily'

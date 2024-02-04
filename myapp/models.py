from django.db import models

# Create your model here
class LongToShort(models.Model):
    long_url = models.URLField(max_length = 500)
    short_url = models.CharField(max_length = 50, unique = True)
    date = models.DateField(auto_now_add = True)
    clicks = models.IntegerField(default = 0)
    dc_licks=models.IntegerField(default=0)
    mc_licks=models.IntegerField(default=0)
    country = models.CharField(max_length=250)
    country_count = models.CharField(max_length=250)
    
    





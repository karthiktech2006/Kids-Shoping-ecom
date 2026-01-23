from django.db import models # type: ignore
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField(null=True )
    image =models.CharField(max_length=50000)
    
    def __str__(self):
        return self.name 
    @property
    def imageUrl(self):
       try:
           return self.image.url
     
       except:        
           return ""
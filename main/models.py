from django.db import models
from datetime import datetime

now = datetime.now()
# Create your models here.

MONTHS =(
    (1,'YANVAR'),
    (2,'FAVRAL'),
    (3,'MART'),
    (4,'APREL'),
    (5,'MAY'),
    (6,'IYUN'),
    (7,'IYUL'),
    (8,'AVGUST'),
    (9,'SENTABR'),
    (10,'OKTABR'),
    (11,'NOYABR'),
    (12,'DEKABR'),

)



class AvansUser(models.Model):
    user_id = models.IntegerField(default=0)
    chat_id = models.IntegerField(default=0)
    name = models.CharField(max_length=100,blank=True,null=True)
    mail = models.CharField(max_length=50,blank=True,null=True)
    modul = models.CharField(max_length=10,blank=True,null=True)
    avans = models.CharField(max_length=25,blank=True,null=True)
    oy = models.SmallIntegerField(default=now.month)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

  
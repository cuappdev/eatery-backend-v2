from django.db import models
from datetime import date

class LoginStore(models.Model):

    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50)
    password_digest = models.CharField(max_length=30)
    #sessionID = models.IntegerField(max_length=64)
    #sessionIDExpiration = models.TimeField()
    #updateToken = models.IntegerField()
    #eatery_id = models.ForeignKey('EateryModel', on_delete = models.DO_NOTHING)

    
        
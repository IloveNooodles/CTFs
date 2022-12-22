from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50) # Consist of hex characters and have 'X' as prefix character
    hobby = models.CharField(max_length=50, blank=True)

    class Meta:
        managed = False
        db_table = 'users'
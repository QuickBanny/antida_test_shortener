from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Link(models.Model):
    short_id = models.SlugField(max_length=6)
    short_link = models.URLField()
    full_link = models.URLField()
    count = models.IntegerField(default=0)
    date_of_creations = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__ (self):
        return self.short_link

from django.db import models
from profiles.models import Profile
# Create your models here.
class Log(models.Model):
    photo = models.ImageField(upload_to="media/logs/")
    is_correct = models.BooleanField(default=False)
    created= models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return f"Log of {self.profile.id}"
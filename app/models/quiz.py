from django.db import models
from django.conf import settings
import datetime


class Quiz(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.datetime.now)
    score = models.IntegerField(null=False)
    questions = models.TextField(default='')
    topic = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.user.__str__() + str(self.date) + str(self.score)

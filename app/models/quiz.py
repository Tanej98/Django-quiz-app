from django.db import models
from django.conf import settings


class Quiz(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    score = models.IntegerField(null=False)

    def __str__(self):
        return self.user.__str__() + str(self.date) + str(self.score)

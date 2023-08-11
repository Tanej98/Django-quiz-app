from django.db import models


class Question(models.Model):
    id = models.BigAutoField(primary_key=True)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255, null=True)
    option2 = models.CharField(max_length=255, null=True)
    option3 = models.CharField(max_length=255, null=True)
    option4 = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.question


from django.db import models


class Question(models.Model):
    """A Django Model class used to represent a Question Object

    Attributes
    ----------
    id : int
        An unique number to represent Question object
    question : str
        The question string
    option1 : str
        The answer option for the question
    option2 : str
        The answer option for the question
    option3 : str
        The answer option for the question
    option4 : str
        The answer option for the question
    answer : str
        The answer for the question
    topic : str
        The questions topic

    """
    id = models.BigAutoField(primary_key=True)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255, null=True)
    option2 = models.CharField(max_length=255, null=True)
    option3 = models.CharField(max_length=255, null=True)
    option4 = models.CharField(max_length=255, null=True)
    topic = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.question


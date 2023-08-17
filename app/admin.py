from django.contrib import admin
from app.models import Question
from app.models import Quiz

# Registering models to admin page.
admin.site.register(Question)
admin.site.register(Quiz)

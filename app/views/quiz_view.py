from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import random
from django.shortcuts import redirect

from app.models.question import Question
from app.models.quiz import Quiz


def quiz(request):
    return render(request=request, template_name="quiz.html")


def redirect_to_dashboard(request):
    if request.method == "POST":
        questions_list = Question.objects.all()
        correct_answers = 0
        for question in questions_list:
            for i in request.POST:
                if i != "csrfmiddlewaretoken":
                    if question.question.strip() == i.strip() and question.answer.strip() == request.POST[i].strip():
                        correct_answers = correct_answers + 1
        q = Quiz(user=request.user, score=correct_answers)
        q.save()
    return redirect('dashboard')

@login_required
def take_quiz(request):
    questions = list(Question.objects.all())
    questions = random.sample(questions, 5)
    return render(request=request, template_name="quiz.html", context={"questions": questions})
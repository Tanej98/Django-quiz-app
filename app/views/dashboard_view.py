from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Min
from app.models.quiz import Quiz
import math

@login_required
def user_dashboard(request):
    last_five_quiz = Quiz.objects.filter(user=request.user).order_by('-date')[:5]
    avg_score = Quiz.objects.filter(user=request.user).aggregate(Avg('score'))
    max_score = Quiz.objects.filter(user=request.user).aggregate(Max('score'))
    min_score = Quiz.objects.filter(user=request.user).aggregate(Min('score'))
    print(last_five_quiz)
    avg_score['score__avg'] = math.floor(avg_score['score__avg'] * 100)/100.0
    print(avg_score)
    print(max_score)
    print(min_score)

    # if request.method == "POST":
    #     questions_list = Question.objects.all()
    #     correct_answers = 0
    #     for question in questions_list:
    #         for i in request.POST:
    #             if i != "csrfmiddlewaretoken":
    #                 if question.question.strip() == i.strip() and question.answer.strip() == request.POST[i].strip():
    #                     correct_answers = correct_answers + 1
    #     q = Quiz(user=request.user, score=correct_answers)
    #     q.save()
    #     print(correct_answers)
    #     last_five_quiz = Quiz.objects.filter(user=request.user).order_by('-date')[:5]
    return render(request=request, template_name="dashboard.html", context={"last_five_quiz": last_five_quiz,
                                                                            'min_score': min_score['score__min'],
                                                                            'max_score': max_score['score__max'],
                                                                            'avg_score': avg_score['score__avg']}
                  )

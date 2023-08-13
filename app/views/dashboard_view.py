from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Min
from app.models.quiz import Quiz
import math
import datetime
from django.http import JsonResponse


def server_time(request):
    now = datetime.datetime.now()
    response_data = {'server_time': now.strftime('%Y-%m-%d %H:%M:%S')}
    return JsonResponse(response_data)

@login_required
def user_dashboard(request):
    last_five_quiz = Quiz.objects.filter(user=request.user).order_by('-date')[:5]

    if len(last_five_quiz) == 0:
        return render(request=request, template_name="dashboard.html", context={'quiz_take': False})
    avg_score = Quiz.objects.filter(user=request.user).aggregate(Avg('score'))
    max_score = Quiz.objects.filter(user=request.user).aggregate(Max('score'))
    min_score = Quiz.objects.filter(user=request.user).aggregate(Min('score'))
    print(last_five_quiz)
    last_quiz = last_five_quiz[0]
    # print(last_five_quiz)
    # print(avg_score)
    # print(max_score)
    # print(min_score)
    if avg_score is not None and avg_score['score__avg'] is not None:
        avg_score['score__avg'] = math.floor(avg_score['score__avg'] * 100) / 100.0
    result_text = ""
    if last_quiz.score == 5:
        result_text = "You are a genius!"
    elif last_quiz.score == 4:
        result_text = "You are smart!"
    elif last_quiz.score == 3:
        result_text = "you are above average"
    else:
        result_text = "Please try again!"
    return render(request=request, template_name="dashboard.html", context={"last_five_quiz": last_five_quiz,
                                                                            'min_score': min_score['score__min'],
                                                                            'max_score': max_score['score__max'],
                                                                            'avg_score': avg_score['score__avg'],
                                                                            'last_quiz_score': (last_quiz.score / 5) * 100,
                                                                            'last_quiz': last_quiz,
                                                                            'quiz_take': True,
                                                                            'result_text': result_text,
                                                                            'retake': (last_quiz.score <= 3)}
                  )

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max, Min
from app.models.quiz import Quiz
import math
from django.http import JsonResponse
from django.core import serializers



def user_name(request):
    response_data = {'username': str(request.user).capitalize()}
    return JsonResponse(response_data)

@login_required
def get_quiz_metrics(request):
    topic = request.GET.get('topic', 'Overall')
    if topic == 'Overall':
        topic = ['Sports', 'Geography', 'Solar System']
    else:
        topic = [topic]
    avg_score = Quiz.objects.filter(user=request.user, topic__in=topic).aggregate(Avg('score'))
    max_score = Quiz.objects.filter(user=request.user, topic__in=topic).aggregate(Max('score'))
    min_score = Quiz.objects.filter(user=request.user, topic__in=topic).aggregate(Min('score'))
    if avg_score['score__avg'] is None:
        avg_score['score__avg'] = -1
        max_score['score__max'] = -1
        min_score['score__min'] = -1
    else:
        if avg_score is not None and avg_score['score__avg'] is not None:
            avg_score['score__avg'] = math.floor(avg_score['score__avg'] * 100) / 100.0

    response_data = {'avg_score': avg_score['score__avg'], 'max_score': max_score['score__max'],
                     'min_score': min_score['score__min']}
    if request.GET.get("all_quizzes", "False") != "False" and topic != "Overall":
        all_quizzes = Quiz.objects.filter(user=request.user, topic=topic).order_by('-date')
        response_data['quizzes'] = serializers.serialize('json', all_quizzes)

    print(response_data)
    return JsonResponse(response_data)

@login_required
def user_dashboard(request):
    last_five_quiz = Quiz.objects.filter(user=request.user).order_by('-date')[:5]

    if len(last_five_quiz) == 0:
        return render(request=request, template_name="dashboard.html", context={'quiz_take': False})

    last_quiz = last_five_quiz[0]
    if last_quiz.score == 5:
        result_text = "You are a genius!"
    elif last_quiz.score == 4:
        result_text = "You are smart!"
    elif last_quiz.score == 3:
        result_text = "you are above average"
    else:
        result_text = "Please try again!"
    return render(request=request, template_name="dashboard.html", context={"last_five_quiz": last_five_quiz,
                                                                            'last_quiz_score': (last_quiz.score / 5) * 100,
                                                                            'last_quiz': last_quiz,
                                                                            'quiz_take': True,
                                                                            'result_text': result_text,
                                                                            'retake': (last_quiz.score < 3)}
                  )

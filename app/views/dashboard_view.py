from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.models.quiz import Quiz

from django.http import JsonResponse


@login_required
def user_name(request):
    """user_name is an authenticate method which returns the current logged-in user's username

    Args:
        request: Httprequest

    Returns:
        return's username
    """
    response_data = {'username': str(request.user).capitalize()}
    return JsonResponse(response_data)


@login_required
def user_dashboard(request):
    """user_dashboard is an authenticate method which renders the user dashboard with last 5 quiz details

    Args:
        request: Httprequest

    Returns:
        render user dashboard template
    """
    last_five_quiz = Quiz.objects.filter(user=request.user).order_by('-date')[:5]

    # if user didn't take any quiz
    if len(last_five_quiz) == 0:
        return render(request=request, template_name="dashboard.html", context={'quiz_take': False})

    # display the last quiz result
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

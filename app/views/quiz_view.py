import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import random
from django.shortcuts import redirect
import json
import math
from django.core import serializers
from django.db.models import Avg, Max, Min
from django.http import JsonResponse
from django.utils.timezone import make_aware

from app.models.question import Question
from app.models.quiz import Quiz


@login_required(login_url='login/')
def get_all_quizzes(request):
    """get_all_quizzes is an authenticated route which gets the topic and returns the all quizzes taken
        on that topic.

        note: default topic Sports

    """
    if request.method == "GET":
        # gets the topic
        topic = request.GET.get('topic', 'Sports')
        all_quizzes = Quiz.objects.filter(user=request.user,topic=topic).order_by('-date')
        return render(request=request, template_name="all_quizzes.html", context={"quizzes": all_quizzes,
                                                                                  "selected_topic": topic})


@login_required(login_url='login/')
def get_quiz(request):
    """get quiz returns the single quiz with all the questions and its write answers and user answers
    """
    try:
        if request.method == "GET":
            # taking quiz id from the get url
            quiz_id = request.GET.get('quiz_id')
            quiz_ = Quiz.objects.filter(pk=quiz_id)
            questions = {}
            question_dict = json.loads(quiz_[0].questions)
            # looping through all the questions
            for i in range(1, 6):
                question = Question.objects.filter(pk=question_dict['question_' + str(i)])
                answer = question_dict['answer_' + str(i)]
                # saving question
                questions["question_" + str(i)] = question[0].question
                questions["correct_answer_" + str(i)] = question[0].answer
                # saving answer
                questions["selected_answer_" + str(i)] = answer

                # if answer is correct make border green else red
                if question[0].answer.strip() == answer.strip():
                    questions["class_" + str(i)] = "border border-success"
                else:
                    questions["class_" + str(i)] = "border border-danger"
            return render(request=request, template_name="modal.html", context=questions)
    except Exception:
        return HttpResponse("<p>Error displaying quiz</p>")

# @login_required
# def quiz(request):
#     return render(request=request, template_name="quiz.html")


@login_required(login_url='login/')
def redirect_to_dashboard(request):
    """redirect_to_dashboard saves the quiz and redirects to dashboard
    """
    if request.method == "POST":
        # validating answers against questions from db
        if "topic" in request.POST:
            questions_list = Question.objects.filter(topic=request.POST["topic"])
        else:
            questions_list = Question.objects.all()
        correct_answers = 0
        questions_dict = {}
        question_count = 1
        topic = ''
        for question in questions_list:
            for i in request.POST:
                if i not in ["csrfmiddlewaretoken",'quiz_id', 'topic']:
                    if question.question.strip() == i.strip():
                        questions_dict['question_'+str(question_count)] = question.id
                        questions_dict['answer_'+str(question_count)] = request.POST[i].strip()
                        topic = question.topic
                        question_count += 1
                        if question.answer.strip() == request.POST[i].strip():
                            correct_answers = correct_answers + 1
        # retry quiz path
        if "topic" in request.POST:
            topic = request.POST["topic"]
        if 'quiz_id' in request.POST:
            q = Quiz.objects.filter(pk=request.POST['quiz_id'])[0]
        else:
            # new quiz
            q = Quiz()
        q.user = request.user
        q.score = correct_answers
        q.questions = json.dumps(questions_dict)
        q.topic = topic
        q.date = make_aware(datetime.datetime.now() + datetime.timedelta(hours=1))
        q.save()
    return redirect('dashboard')


@login_required(login_url='/accounts/login/')
def take_quiz(request):
    """take_quiz renders quiz either new or old one
    """
    topic = 'Sports'
    if request.method == "GET":
        # check if we have quiz id to load old quiz
        quiz_id = request.GET.get('quiz', -1)
    if request.method == "POST" and 'topic' in request.POST:
        # render new quiz
        topic = request.POST['topic']
        quiz_id = -1
    if quiz_id == -1:
        # rendering new quiz
        questions = list(Question.objects.filter(topic=topic))
        # selecting 5 random questions
        questions = random.sample(questions, 5)
        topic = questions[0].topic
    else:
        # rendering old quiz
        quiz_ = Quiz.objects.get(pk=quiz_id)
        topic = quiz_.topic
        question_dict = json.loads(quiz_.questions)
        question_ids = []
        for i in range(1, 6):
            question_ids.append(question_dict['question_'+str(i)])
        questions = Question.objects.filter(pk__in=question_ids)
    return render(request=request, template_name="quiz.html", context={"questions": questions, 'quiz_id': quiz_id,
                                                                       'topic': topic})


@login_required(login_url='login/')
def get_quiz_metrics(request):
    """
    get_quiz_metrics returns json response of max,min,avg score
    """
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
    return JsonResponse(response_data)

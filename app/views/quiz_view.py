import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import random
from django.shortcuts import redirect
import json
from app.models.question import Question
from app.models.quiz import Quiz


def quiz(request):
    return render(request=request, template_name="quiz.html")


def redirect_to_dashboard(request):
    if request.method == "POST":
        questions_list = Question.objects.all()
        correct_answers = 0

        questions_dict = {}
        question_count = 1
        for question in questions_list:
            for i in request.POST:
                if i != "csrfmiddlewaretoken" or i != 'quiz_id':
                    if question.question.strip() == i.strip():
                        questions_dict['question_'+str(question_count)] = question.id
                        questions_dict['answer_'+str(question_count)] = request.POST[i].strip()
                        question_count += 1
                        if question.answer.strip() == request.POST[i].strip():
                            correct_answers = correct_answers + 1
        if 'quiz_id' in request.POST:
            q = Quiz.objects.filter(pk=request.POST['quiz_id'])[0]
            q.date = datetime.datetime.now()
        else:
            q = Quiz()
        q.user = request.user
        q.score = correct_answers
        q.questions = json.dumps(questions_dict)
        q.save()
    return redirect('dashboard')


@login_required
def take_quiz(request):
    quiz_id = request.GET.get('quiz', -1)
    if quiz_id == -1:
        questions = list(Question.objects.all())
        questions = random.sample(questions, 5)
    else:
        quiz_ = Quiz.objects.get(pk=quiz_id)
        question_dict = json.loads(quiz_.questions)
        question_ids = []
        for i in range(1,6):
            question_ids.append(question_dict['question_'+str(i)])
        questions = Question.objects.filter(pk__in=question_ids)
    return render(request=request, template_name="quiz.html", context={"questions": questions, 'quiz_id': quiz_id})

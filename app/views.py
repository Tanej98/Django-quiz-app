from django.shortcuts import render, redirect
from app.forms.user_register_form import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import random

from app.models.question import Question
from app.models.quiz import Quiz


def homepage(request):
    return render(request=request, template_name="homepage.html")


def user_registration(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="register.html", context={"register_form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password.")
                return redirect("/homepage")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def quiz(request):
    return render(request=request, template_name="quiz.html")


@login_required
def user_dashboard(request):
    if request.method == "POST":
        questions_list = Question.objects.all()
        correct_answers = 0
        for question in questions_list:
            for i in request.POST:
                if i != "csrfmiddlewaretoken":
                    if question.question.strip() == i.strip() and question.answer.strip() == request.POST[i].strip():
                        correct_answers = correct_answers + 1
        q = Quiz(user=request.user,score=correct_answers)
        q.save()
        print(correct_answers)
    return render(request=request, template_name="dashboard.html")

@login_required
def take_quiz(request):
    questions = list(Question.objects.all())
    questions = random.sample(questions, 5)
    return render(request=request, template_name="quiz.html", context={"questions": questions})

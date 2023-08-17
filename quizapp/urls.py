"""
URL configuration for quizapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name="homepage"),
    path('login/', user_login, name="login"),
    path('logout/', logout_view, name="logout"),
    path('quiz/', take_quiz, name="quiz"),
    path('quiz_metrics/', get_quiz_metrics, name="quiz_metrics"),
    path('quiz/dashboard', redirect_to_dashboard),
    path('dashboard/', user_dashboard, name="dashboard"),
    path('register/', user_registration, name="register"),
    path('user_name/', user_name, name="user_name"),
    path('all_quizzes/', get_all_quizzes, name="all_quizzes"),
    path("get_quiz/", get_quiz, name="get_quiz")
]

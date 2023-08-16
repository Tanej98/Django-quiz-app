from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import logout
from django.shortcuts import redirect


def logout_view(request):
    logout(request)
    return redirect('homepage')


def homepage(request):
    user_cs = request.GET.get("user_cs", False)
    return render(request=request, template_name="homepage.html", context={"user_cs": user_cs})

def user_login(request):
    form = AuthenticationForm()
    auth_error = False
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
                auth_error = False
    return render(request=request, template_name="login.html", context={"login_form": form, "auth_error": auth_error})

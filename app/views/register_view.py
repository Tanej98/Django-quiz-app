from django.shortcuts import render
from app.forms.user_register_form import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect, reverse


def user_registration(request):
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.", "success")
            return redirect('{}?user_cs=True'.format(reverse('homepage')))

    return render(request=request, template_name="register.html", context={"register_form": form})
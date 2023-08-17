from django.shortcuts import render
from app.forms.user_register_form import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect, reverse


def user_registration(request):
    """user_registration renders user registration form
    """
    form = NewUserForm()
    if request.method == "POST":
        # initialize new form
        form = NewUserForm(request.POST)
        if form.is_valid():
            # if form is valid save the user to db
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.", "success")
            # redirect to homepage
            # user_cs variable is used to show the success notification on the homepage
            return redirect('{}?user_cs=True'.format(reverse('homepage')))

    return render(request=request, template_name="register.html", context={"register_form": form})

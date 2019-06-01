from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
from .registration import Registration
from django.contrib.auth import login, authenticate


# it will create user and save it to database
def sign_up(request):
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = Registration()
    return render(request, 'registration/signup.html', {'form': form})


# it will delete user from database
def delete_user(request, id):
    user = get_object_or_404(User, pk=id)
    for post in user.blogmodel_set.all():
        post.image.delete()
    user.delete()
    return redirect('index')

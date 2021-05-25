from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.exceptions import FieldError
from django.views.decorators.csrf import csrf_exempt

import json

from .models import *


# Create your views here.

def index(request):
    return render(request, "shareaccbook/index.html")

@login_required(login_url='login')
def createAccBook(request):
    # create form
    form = createAccBookForm()

    # check request method
    if request.method == 'POST':
        form = createAccBookForm(request.POST)

        if form.is_valid():
            # get user
            newForm = form.save(commit=False)
            newForm.owner = request.user
            newForm.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            message = "Something wrong. Please try again."
            return render(request, "shareaccbook/createAccBook.html", {
                'form': form,
                'message': message
                })
    return render(request, "shareaccbook/createAccBook.html", {
        "form": form
    })

def login_view(request):
    if request.method == "POST":
        #Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        #Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "shareaccbook/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "shareaccbook/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        #Check password
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "shareaccbook/register.html", {
                "message": "Passwords not match. Please try again."
            })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "shareaccbook/register.html", {
                "message": "Username already existed."
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "shareaccbook/register.html")

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

@login_required
def createAccBook(request):
    # check request method
    if request.method == "GET":
        form = createAccBookForm()
        return render(request, "shareaccbook/createAccBook.html", {
            "form": form
        })
    elif request.method == "POST":
        # Get info of acc book
        data = json.loads(request.body)
        accbook_type = data.get('book_type')
        accbook_name = data.get('book_name')
        owner = User.objects.get(username=request.user)

        # try to create new acc book
        try:
            new_book = UserAccBook.objects.create(owner=owner, accbook_type=accbook_type, accbook_name=accbook_name)
            new_book.save()
        except UserAccBook.FieldError:
            error = "'Account book already existed. Please try another name.'"
            return JsonResponse({"error": error})
        
        return JsonResponse({
            "message": "Account book created successfully.",
            "data": {
                "owner": owner,
                "accbook_type": accbook_type,
                "accbook_name": accbook_name
            }
            })
    else:
        return JsonResponse({"error": "Invalid request."}, status=400)

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

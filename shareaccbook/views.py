from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.exceptions import FieldError

from .models import User, UserAccBook, AccBookItem, SharedUser

# Create your views here.

def index(request):
    return render(request, "shareaccbook/index.html")

@login_required
def createAccBook(request):
    if request.method == 'POST':
        #Get acc book information
        owner = request.POST["owner"]
        accbook_type = request.POST["type"]
        accbook_name = request.POST["accbook_name"]

        #get user from db
        try:
            user = User.objects.get(username=owner)
        except User.DoesNotExist:
            return render(request, "shareaccbook/createAccBook.html", {
                "message": "User does not exist. Please try again."
            })
        try: 
            newAccBook = UserAccBook.objects.create(owner=owner, accbook_type=accbook_type, accbook_name=accbook_name)
            newAccBook.save()
        except FieldError:
            return render(request, "user/createAccBook.html", {
                "message": "Error occured. Please try again."
            })
    else:
        return render(request, "shareaccbook/nopermissionerror.html")
    return

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

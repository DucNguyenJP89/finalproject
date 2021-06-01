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

            #get created accbook
            owner = User.objects.get(username=request.user)
            accbook_type = form.cleaned_data['accbook_type']
            accbook_name = form.cleaned_data['accbook_name']

            userAccBook = UserAccBook.objects.get(owner=owner, accbook_type=accbook_type, accbook_name=accbook_name)

            acc_id = userAccBook.id
            
            return HttpResponseRedirect(reverse("accBookView", args=[acc_id]))
        else:
            message = "Something wrong. Please try again."
            return render(request, "shareaccbook/createAccBook.html", {
                'form': form,
                'message': message
                })
    return render(request, "shareaccbook/createAccBook.html", {
        "form": form
    })

@login_required(login_url="login")
def accBookView(request, acc_id):
    # get accbook with acc_id
    try:
        accBook = UserAccBook.objects.get(pk=acc_id)
        if accBook.owner != request.user:
            return render(request, "shareaccbook/AccBookItems.html", {
                "message": "You are not allowed to view this accbook. Please contact the owner for permission."
            })
    except UserAccBook.DoesNotExist:
        return render(request, "shareaccbook/AccBookItems.html", {
            "message": "Account book not found."
        })

    # get items of accbook
    items = AccBookItem.objects.filter(acc_book_id=acc_id)

    # create form create new item
    form = createNewItemForm()

    if request.method == "POST":
        form = createNewItemForm(request.POST)
        if form.is_valid():
            newItem = form.save(commit=False)
            newItem.user_id = request.user
            newItem.acc_book_id = accBook
            newItem.save()
            
            return HttpResponseRedirect(reverse("accBookView", args=[acc_id]))
        else:
            return render(request, "shareaccbook/AccBookItems.html", {
                "accBook": accBook,
                "form": form,
                "items": items,
                "form_message": "Cannot create new item. Please try again."
            })

    return render(request, "shareaccbook/AccBookItems.html", { 
        "accBook": accBook,
        "form": form, 
        "items": items
        })

@login_required(login_url='login')
def createNewItem(request, acc_id):
    # Only use with method post
    if request.method != 'POST':
        return render(request, "shareaccbook/index.html", {
            "message": "Error occured. Please try again."
        })
    
    # get accbook 
    accBook = UserAccBook.objects.get(pk=acc_id)
    if accBook is None:
        return render(request, "shareaccbook/index.html", {
            "message": "Error occured. Please try again."
        })
    
    # create form with information from POST request
    form = createNewItemForm(request.POST)

    if form.is_valid():
        newItem = form.save(commit=False)
        newItem.user_id = request.user
        newItem.save()
        
        return HttpResponseRedirect(reverse("accBookView", args=[acc_id]))
    else:
        initialForm = createNewItemForm()
        # get items of accbook
        items = AccBookItem.objects.filter(acc_book_id=acc_id)
        return render(request, "shareaccbook/AccBookItems.html", {
            "accBook": accBook,
            "form": initialForm,
            "items": items,
            "form_message": "Cannot create new item. Please try again."
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

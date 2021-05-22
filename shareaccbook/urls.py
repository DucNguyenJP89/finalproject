from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    #registration path
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API routes: account book
    path("accbook/create", views.createAccBook, name="createAccBook"),

]
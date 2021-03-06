from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    #registration path
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # route: create acc book
    path("accbook/create", views.createAccBook, name="createAccBook"),
    # route: acc book view
    path("accbook/<int:acc_id>", views.accBookView, name="accBookView"),

]
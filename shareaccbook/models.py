from django.db import models
from django.contrib.auth.models import AbstractUser

import datetime

# Create your models here.
class User(AbstractUser):
    pass

# account_type
BOOK_TYPE = (
    (1, "Household"),
    (2, "Travel"),
    (3, "Others")
)

class UserAccBook(models.Model):
    owner = models.OneToOneField("User", on_delete=models.CASCADE, related_name="accbook_creator")
    view_users = models.ManyToManyField("User", related_name="view_only_users")
    edit_users = models.ManyToManyField("User", related_name="can_edit_users")
    accbook_type = models.IntegerField(choices=BOOK_TYPE, default=1)
    accbook_name = models.CharField(max_length=50, blank=False)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        created_on = self.created_on.strftime("%b %-d %Y, %_I:%M %p")
        return f"{self.accbook_name} created by {self.owner} at {created_on}"

ITEM_TYPE = (
    ("Housing", (
        (1, "Rent"),
        (2, "House Loan")
    )),
    ("Ultilities", (
        (3, "Water bill"),
        (4, "Electricity"),
        (5, "Gas"),
        (6, "Phone/Internet")
    )),
    ("Food", (
        (7, "Eating out"),
        (8, "Groceries"),
        (9, "Snacks")
    )),
    ("Leisure", (
        (10, "Clothes"),
        (11, "Cosmetics"),
        (12, "Movies"),
        (13, "Other leisures")
    )),
    ("Others", "Others")
)

class AccBookItem(models.Model):
    acc_book_id = models.ForeignKey("UserAccBook", on_delete=models.CASCADE, related_name="belonging_accbook")
    regist_date = models.DateField(default=datetime.date.today())
    modified_date = models.DateField(auto_now_add=True)
    item_type = models.IntegerField(choices=ITEM_TYPE, blank=False)
    item_description = models.CharField(max_length=50)
    item_price = models.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        ordering = ['-regist_date']
    
    def __str__(self):
        return f"New item: {self.item_type} created at {self.regist_date}."




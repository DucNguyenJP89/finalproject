from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm, CharField

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
    owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="accbook_creator")
    accbook_type = models.IntegerField(choices=BOOK_TYPE, default=1)
    accbook_name = models.CharField(max_length=50, blank=False)
    created_on = models.DateField(default=datetime.date.today)
    updated_on = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        created_on = self.created_on.strftime("%b %-d %Y, %_I:%M %p")
        return f"{self.accbook_name} created by {self.owner} at {created_on}"

class createAccBookForm(ModelForm):
    class Meta:
        model = UserAccBook
        fields = ['accbook_type', 'accbook_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['accbook_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['accbook_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Accbook Name'})

# User access types
USER_PERMISSIONS = (
    (0, "No permission"),
    (1, "Can view"),
    (2, "Can edit")
)

class SharedUser(models.Model):
    acc_book_id = models.ForeignKey("UserAccBook", on_delete=models.CASCADE, related_name="shared_users")
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    user_permissions = models.IntegerField(choices=USER_PERMISSIONS, default=0)

# Items type
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

EXPENSE_TYPE = (
    (1, "Income"),
    (2, "Expense")
)

class AccBookItem(models.Model):
    acc_book_id = models.ForeignKey("UserAccBook", on_delete=models.CASCADE, related_name="belonging_accbook")
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    regist_date = models.DateField(default=datetime.date.today)
    modified_date = models.DateField(auto_now=True)
    expense_type = models.IntegerField(choices=EXPENSE_TYPE, default=2)
    item_type = models.IntegerField(choices=ITEM_TYPE, blank=False)
    item_description = models.CharField(max_length=50)
    item_price = models.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        ordering = ['-regist_date']
    
    def __str__(self):
        return f"New item: {self.item_type} created at {self.regist_date}."

class createNewItem(ModelForm):
    class Meta:
        model = AccBookItem
        fields = ['regist_date', 'expense_type', 'item_type', 'item_price', 'item_description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['expense_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['item_type'].widget.attrs.update({'class': 'form-select'})
        self.fields['item_price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'How much?'})
        self.fields['item_description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'More details (50 characters)'})




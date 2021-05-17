from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils import timezone

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
    accbook_type = models.IntegerField(choices=BOOK_TYPE, default=1)
    accbook_name = models.CharField(max_length=50, blank=False)
    created_on = models.DateField(default=timezone.now())
    updated_on = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        created_on = self.created_on.strftime("%b %-d %Y, %_I:%M %p")
        return f"{self.accbook_name} created by {self.owner} at {created_on}"

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

class AccBookItem(models.Model):
    acc_book_id = models.ForeignKey("UserAccBook", on_delete=models.CASCADE, related_name="belonging_accbook")
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    regist_date = models.DateField(default=timezone.now())
    modified_date = models.DateField(auto_now_add=True)
    item_type = models.IntegerField(choices=ITEM_TYPE, blank=False)
    item_description = models.CharField(max_length=50)
    item_price = models.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        ordering = ['-regist_date']
    
    def __str__(self):
        return f"New item: {self.item_type} created at {self.regist_date}."




from django.db import models
from django.contrib.auth.models import AbstractUser

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
    shared_users = models.ManyToManyField("User", related_name="shared_users")
    accbook_type = models.IntegerField(choices=BOOK_TYPE, default=1)
    accbook_name = models.CharField(max_length=50, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
    
    def __str__(self):
        created_on = self.created_on.strftime("%b %-d %Y, %_I:%M %p")
        return f"{self.accbook_name} created by {self.owner} at {created_on}"


